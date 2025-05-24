import hashlib
from datetime import datetime
from typing import Dict, List

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from agno.document.base import Document

from utils.logger import get_logger

logger = get_logger(__name__)
today_str = datetime.now().strftime("%Y-%m-%d")


def hash_content(content: str) -> str:
    """
    Compute a SHA-256 hash of the given text content.

    This is used to identify and skip duplicate pages during the crawl.

    Parameters:
        content (str): The text content to hash.

    Returns:
        str: The SHA-256 hash of the input string.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


async def crawl_website_for_documents(
    website_url: str,
    metadata: Dict = None,
    max_depth: int = 5,
    word_count_threshold: int = 200,
) -> List[Document]:
    """
    Asynchronously crawls a website and returns a list of deduplicated, cleaned `Document` objects.

    This function uses a BFS deep crawling strategy and filters out pages with low content or
    duplicate text. HTML content is converted to Markdown before being packaged as a agno
    `Document`.

    Parameters:
        website_url (str): The root URL to start crawling from.
        metadata (Dict, optional): Additional metadata to attach to each `Document`.
        max_depth (int, optional): Maximum link-following depth for the crawl. Default is 5.
        word_count_threshold (int, optional): Minimum number of words required to retain a page. Default is 200.

    Returns:
        List[Document]: A list of agno `Document` objects with `page_content` and associated metadata.

    Notes:
        - Duplicate documents (based on text hash) are skipped.
        - Empty or non-substantive pages are ignored.
        - Metadata includes crawl depth, source URL, and crawl date.
    """
    metadata = metadata or {}
    logger.info(f"Starting deep crawl of {website_url}")

    # Initialize Markdown generator with options for cleaner output
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "ignore_images": True,
            "escape_html": False,
            "body_width": 80,
            "skip_internal_links": True,
            "include_sup_sub": True,
        }
    )

    # Configure the crawling run
    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth,
            include_external=False,
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        word_count_threshold=word_count_threshold,
        scan_full_page=True,
        process_iframes=True,
        simulate_user=True,
        exclude_external_links=True,
        exclude_social_media_links=True,
    )

    cleaned_docs = []
    seen_hashes = set()

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(website_url, config=config)
        logger.info(f"Crawled {len(results)} pages")

        for result in results:
            text = result.markdown
            url = result.url

            if not text:
                logger.warning(f"Empty text skipped: {url}")
                continue

            content_hash = hash_content(text.strip())
            if content_hash in seen_hashes:
                logger.info(f"Duplicate content skipped: {url}")
                continue
            seen_hashes.add(content_hash)

            doc_metadata = {
                "source": url,
                "markdown": text,
                "depth": result.metadata.get("depth", 0),
                "website": website_url,
                "parsing_date": today_str,
            }
            doc_metadata.update(metadata)

            cleaned_docs.append(Document(content=text, meta_data=doc_metadata, name="GG"))

    logger.info(f"Returning {len(cleaned_docs)} documents")
    return cleaned_docs
