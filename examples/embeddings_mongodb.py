import os

from components.embedding.vectorstore.mongodb_store import MongoDBVectorStoreFactory
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings

# === Step 1: Prepare Environment Variables ===
os.environ["ATLAS_CONNECTION_STRING"] = "your_mongodb_connection_string"
os.environ["ATLAS_DB"] = "your_database"
os.environ["ATLAS_COLLECTION"] = "your_collection"
os.environ["ATLAS_INDEX"] = "your_index"

# === Step 2: Load Embedding Model ===
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# === Step 3: Create the MongoDB Vector Store Factory ===
vector_store_factory = MongoDBVectorStoreFactory(embedding_model=embedding_model)

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

# === Step 5: Index the Documents ===
vector_store_factory.from_documents(documents)
print("✅ Documents indexed successfully.")

# === Step 6: Perform Similarity Search ===
query = "What is a vector database?"
results = vector_store_factory.similarity_search_with_score(query=query, k=2)

# === Step 7: Display Results ===
print("\n🔍 Similarity Search Results:")
for doc, score in results:
    print(f"\nContent: {doc.page_content}\nScore: {score:.4f}")
