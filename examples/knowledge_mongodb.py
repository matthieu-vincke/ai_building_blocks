import time
from dotenv import load_dotenv
from components.embedding.vectorstore.mongodb_store import MongoDBVectorStoreFactory
from agno.document.base import Document
from agno.knowledge.document import DocumentKnowledgeBase

# https://docs.agno.com/vectordb/mongodb

# Import logger
from utils.logger import get_logger
logger = get_logger(__name__)

MONGO_DB="VectorStore"
MONGO_COLLECTION="Embeddings"
MONGO_INDEX="vector_index"

# Load environment variables from .env file
load_dotenv()

logger.info("Loaded environment variables from .env file.")

documents = [
    Document(
        page_content="LangChain is a framework for developing LLM-powered applications.",
        metadata={"source": "langchain"},
    ),
    Document(
        page_content="MongoDB Atlas is a fully managed cloud database.",
        metadata={"source": "mongodb"},
    ),
    Document(
        page_content="Vector databases are optimized for semantic search.",
        metadata={"source": "vector-db"},
    ),
]
logger.info(f"{len(documents)} documents prepared for indexing.")
