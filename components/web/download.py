import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from components.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".txt",
    ".md",
    ".rtf",
    ".odt",
]


def download_documents(
    html_text: str,
    base_url: str,
    download_folder: str,
    extensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Parses HTML content, finds document links, downloads them to a folder, and logs results.

    Args:
        html_text (str): Raw HTML content.
        base_url (str): Base URL for resolving relative links.
        download_folder (str): Folder to store downloaded documents.
        extensions (List[str], optional): List of allowed file extensions.

    Returns:
        Dict: {
            "downloaded": List[str],   # paths of successfully downloaded files
            "failed": List[Dict[str, str]]  # failed attempts with error messages
        }
    """
    extensions = extensions or DEFAULT_EXTENSIONS
    os.makedirs(download_folder, exist_ok=True)

    soup = BeautifulSoup(html_text, "html.parser")
    links = soup.find_all("a", href=True)

    downloaded = []
    failed = []

    for link in links:
        href = link["href"]
        if any(href.lower().endswith(ext) for ext in extensions):
            full_url = urljoin(base_url, href)
            filename = os.path.basename(href.split("?")[0])
            file_path = os.path.join(download_folder, filename)

            logger.info(f"Attempting to download: {full_url}")
            try:
                response = requests.get(full_url, timeout=10)
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(response.content)
                logger.info(f"Downloaded: {file_path}")
                downloaded.append(file_path)
            except requests.RequestException as e:
                error_msg = f"Download error for {full_url}: {str(e)}"
                logger.error(error_msg)
                failed.append({"url": full_url, "error": str(e)})
            except Exception as e:
                error_msg = f"Unexpected error saving {file_path}: {str(e)}"
                logger.error(error_msg)
                failed.append({"url": full_url, "error": str(e)})

    return {"downloaded": downloaded, "failed": failed}
