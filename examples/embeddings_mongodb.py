import time
from dotenv import load_dotenv
from components.embedding.vectorstore.mongodb_store import MongoDBVectorStoreFactory
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Import logger
from utils.logger import get_logger
logger = get_logger(__name__)

MONGO_DB="VectorStore"
MONGO_COLLECTION="Embeddings"
MONGO_INDEX="vector_index"

# Load environment variables from .env file
load_dotenv()

logger.info("Loaded environment variables from .env file.")

# === Step 2: Load Embedding Model ===
logger.info("Loading HuggingFace embedding model...")
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
logger.info("Embedding model loaded.")

# === Step 3: Create the MongoDB Vector Store Factory ===
logger.info("Initializing MongoDB vector store factory...")
vector_store_factory = MongoDBVectorStoreFactory(embedding_model=embedding_model, db_name=MONGO_DB, collection_name=MONGO_COLLECTION, index_name=MONGO_INDEX)
logger.info("MongoDB vector store factory initialized.")

# === Step 4: Sample Documents to Index ===
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

# === Step 5: Index the Documents ===
logger.info("Indexing documents into the vector store...")
vector_store_factory.from_documents(documents)
logger.info("Documents indexed successfully.")

# Wait for indexing to propagate
logger.info("Waiting 5 seconds to allow indexing to complete...")
time.sleep(5)

# === Step 6: Perform Similarity Search ===
query = "What is a vector database?"
logger.info(f"Performing similarity search for query: '{query}'")
results = vector_store_factory.similarity_search_with_score(query=query)
logger.info("Similarity search completed.")

# === Step 7: Display Results ===
logger.info("\n🔍 Similarity Search Results:")
for doc, score in results:
    logger.info(f"Search result: {doc.page_content[:60]}... (score: {score:.4f})")
