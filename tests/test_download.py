import os

import pytest
import requests
import requests_mock

from components.web.download import download_documents

HTML_TEMPLATE = """
<html>
    <body>
        <a href="{file1}">Download PDF</a>
        <a href="{file2}">Download TXT</a>
        <a href="{file3}">Broken DOC</a>
    </body>
</html>
"""

BASE_URL = "https://example.com/"


@pytest.fixture
def mock_html():
    return HTML_TEMPLATE.format(
        file1="docs/file1.pdf", file2="docs/file2.txt", file3="docs/file3.doc"
    )


def test_successful_downloads(mock_html, tmp_path):
    with requests_mock.Mocker() as m:
        # Mock successful responses
        m.get(BASE_URL + "docs/file1.pdf", content=b"%PDF-1.4", status_code=200)
        m.get(BASE_URL + "docs/file2.txt", content=b"hello world", status_code=200)
        m.get(BASE_URL + "docs/file3.doc", status_code=404)

        result = download_documents(
            html_text=mock_html,
            base_url=BASE_URL,
            download_folder=str(tmp_path),
            extensions=[".pdf", ".txt", ".doc"],
        )

        # Check downloaded files
        assert len(result["downloaded"]) == 2
        assert tmp_path.joinpath("file1.pdf").exists()
        assert tmp_path.joinpath("file2.txt").exists()

        # Check failure info
        assert len(result["failed"]) == 1
        assert result["failed"][0]["url"].endswith("file3.doc")
        assert "404" in result["failed"][0]["error"]


def test_no_matching_files(tmp_path):
    html = """
    <html><body>
        <a href="style.css">CSS File</a>
        <a href="image.jpg">Image</a>
    </body></html>
    """
    result = download_documents(
        html_text=html, base_url=BASE_URL, download_folder=str(tmp_path)
    )
    assert result["downloaded"] == []
    assert result["failed"] == []


def test_invalid_url(mock_html, tmp_path):
    with requests_mock.Mocker() as m:
        # Simulate connection error
        m.get(
            BASE_URL + "docs/file1.pdf",
            exc=requests.exceptions.ConnectionError("Connection failed"),
        )
        m.get(BASE_URL + "docs/file2.txt", status_code=200, content=b"text")
        m.get(BASE_URL + "docs/file3.doc", status_code=200, content=b"data")

        result = download_documents(
            html_text=mock_html,
            base_url=BASE_URL,
            download_folder=str(tmp_path),
            extensions=[".pdf", ".txt", ".doc"],
        )

        assert len(result["downloaded"]) == 2
        assert len(result["failed"]) == 1
        assert "Connection failed" in result["failed"][0]["error"]
