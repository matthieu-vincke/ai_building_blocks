import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from langchain.schema import Document

from components.web.deep_crawler import crawl_website_for_documents


@pytest.mark.asyncio
async def test_crawl_returns_documents():
    mock_result = AsyncMock()
    mock_result.markdown = "# Title\n\nSome content."
    mock_result.url = "https://example.com/page1"
    mock_result.metadata = {"depth": 2}

    with patch("components.web.deep_crawler.AsyncWebCrawler") as MockCrawler:
        instance = MockCrawler.return_value.__aenter__.return_value
        instance.arun.return_value = [mock_result]

        documents = await crawl_website_for_documents("https://example.com")

        assert isinstance(documents, list)
        assert len(documents) == 1
        assert isinstance(documents[0], Document)
        assert "source" in documents[0].metadata
        assert "page1" in documents[0].metadata["source"]
        assert "# Title" in documents[0].page_content


@pytest.mark.asyncio
async def test_crawl_filters_empty_and_duplicates():
    mock_result_1 = AsyncMock()
    mock_result_1.markdown = "Unique content"
    mock_result_1.url = "https://example.com/page1"
    mock_result_1.metadata = {"depth": 1}

    mock_result_2 = AsyncMock()
    mock_result_2.markdown = "Unique content"  # Duplicate content
    mock_result_2.url = "https://example.com/page2"
    mock_result_2.metadata = {"depth": 2}

    mock_result_3 = AsyncMock()
    mock_result_3.markdown = ""  # Empty content
    mock_result_3.url = "https://example.com/page3"
    mock_result_3.metadata = {"depth": 3}

    with patch("components.web.deep_crawler.AsyncWebCrawler") as MockCrawler:
        instance = MockCrawler.return_value.__aenter__.return_value
        instance.arun.return_value = [mock_result_1, mock_result_2, mock_result_3]

        documents = await crawl_website_for_documents("https://example.com")
        assert len(documents) == 1
        assert documents[0].metadata["source"] == "https://example.com/page1"


@pytest.mark.asyncio
async def test_metadata_merging():
    mock_result = AsyncMock()
    mock_result.markdown = "Some unique content"
    mock_result.url = "https://example.com/merge"
    mock_result.metadata = {"depth": 1}

    custom_meta = {"source_type": "news", "campaign": "test-run"}

    with patch("components.web.deep_crawler.AsyncWebCrawler") as MockCrawler:
        instance = MockCrawler.return_value.__aenter__.return_value
        instance.arun.return_value = [mock_result]

        documents = await crawl_website_for_documents("https://example.com", metadata=custom_meta)

        doc_meta = documents[0].metadata
        assert doc_meta["source_type"] == "news"
        assert doc_meta["campaign"] == "test-run"
        assert doc_meta["source"] == "https://example.com/merge"
