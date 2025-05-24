import os
from dotenv import load_dotenv
from agno.document.base import Document
from agno.knowledge.document import DocumentKnowledgeBase
from agno.agent import Agent
from agno.vectordb.mongodb import MongoDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
import asyncio

from components.web.deep_crawler import crawl_website_for_documents

# Import logger
from utils.logger import get_logger
logger = get_logger(__name__)

# Load environment variables from .env file
load_dotenv()
logger.info("Loaded environment variables from .env file.")

async def main(recreate: bool = False):
    """
    Main asynchronous function to run the web crawling, indexing, and agent interaction.
    """
    logger.info("Starting web crawling process...")
    documents = []
    if recreate == True:
        logger.info("Recreating the knowledge base index as requested.")
        documents = await crawl_website_for_documents(
            website_url="https://gluegang.co.uk/",
            metadata={"source": "gluegang.co.uk"},
            max_depth=2,
            word_count_threshold=200,
        )

        logger.info(f"{len(documents)} documents prepared for indexing.")

    # Create a DocumentKnowledgeBase instance
    logger.info("Initializing DocumentKnowledgeBase...")
    knowledge_base = DocumentKnowledgeBase(
        documents=documents,
        vector_db=MongoDb(
            embedder = SentenceTransformerEmbedder(),
            collection_name=os.getenv("MONGO_COLLECTION", "crawl-store-query"), # Use os.getenv with default
            db_url=os.getenv("MONGO_CONNECTION_STRING"),
            database=os.getenv("MONGO_DB", "AI_Worflows"), # Use os.getenv with default
            wait_until_index_ready_in_seconds=30,
            wait_after_insert_in_seconds=30
        ),
    )
    logger.info("DocumentKnowledgeBase initialized.")

    logger.info("Loading knowledge base (and potentially recreating index)...")


    logger.info("Initializing Agent...")
    agent = Agent(
        knowledge=knowledge_base,
        search_knowledge=True,
    )
    logger.info("Agent initialized.")

    agent.knowledge.load(recreate=recreate)
    logger.info("Knowledge base loaded.")

    logger.info("Asking the agent: 'What is GlueGang?'")

    agent.print_response("What is GlueGang?")
    logger.info("Agent response received.")

if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main(recreate=True))  # Set recreate to True to recreate the index