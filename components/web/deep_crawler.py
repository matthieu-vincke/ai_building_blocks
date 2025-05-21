import hashlib
from datetime import datetime
from typing import List, Dict

from langchain.schema import Document
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

from components.utils.logger import get_logger

logger = get_logger(__name__)
today_str = datetime.now().strftime("%Y-%m-%d")


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


async def crawl_website_for_documents(
    website_url: str,
    metadata: Dict = None,
    max_depth: int = 5,
    word_count_threshold: int = 200,
) -> List[Document]:
    """
    Crawl a website and return a list of cleaned LangChain Document objects.

    :param website_url: The base URL to crawl
    :param metadata: Optional static metadata to attach to each Document
    :param max_depth: Maximum depth for BFS crawling
    :param word_count_threshold: Minimum words to include a page
    :return: List of langchain.schema.Document objects
    """
    metadata = metadata or {}
    logger.info(f"Starting deep crawl of {website_url}")

    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "ignore_images": True,
            "escape_html": False,
            "body_width": 80,
            "skip_internal_links": True,
            "include_sup_sub": True
        }
    )

    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=max_depth, include_external=False),
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

            cleaned_docs.append(Document(page_content=text, metadata=doc_metadata))

    logger.info(f"Returning {len(cleaned_docs)} documents")
    return cleaned_docs
