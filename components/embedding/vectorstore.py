import os

from langchain.schema import Document
from langchain_mongodb import MongoDBAtlasVectorSearch

# Map store types to constructor functions
VECTOR_STORE_REGISTRY = {}


def register_vector_store(name):
    """
    Decorator to register a new vector store backend.
    """

    def wrapper(cls):
        VECTOR_STORE_REGISTRY[name] = cls
        return cls

    return wrapper


@register_vector_store("mongodb")
class MongoDBVectorStoreFactory:
    @staticmethod
    def create(embedding_model, **kwargs):
        connection_string = kwargs.get("connection_string") or os.getenv(
            "ATLAS_CONNECTION_STRING"
        )
        database = kwargs.get("database") or os.getenv("ATLAS_DB")
        collection = kwargs.get("collection") or os.getenv("ATLAS_COLLECTION")
        index_name = kwargs.get("index_name") or os.getenv("ATLAS_INDEX")

        if not all([connection_string, database, collection, index_name]):
            raise ValueError("Missing MongoDB Atlas config.")

        return MongoDBAtlasVectorSearch.from_connection_string(
            connection_string,
            f"{database}.{collection}",
            embedding_model,
            index_name=index_name,
        )


def create_vector_store(store_type="mongodb", embedding_model=None, **kwargs):
    """
    Factory method to create a vector store.

    :param store_type: The type of vector store (e.g., 'mongodb')
    :param embedding_model: The embedding model to use
    :param kwargs: Optional overrides (connection string, DB name, etc.)
    :return: Vector store instance
    """
    if store_type not in VECTOR_STORE_REGISTRY:
        raise ValueError(f"Unsupported vector store type: {store_type}")

    factory_class = VECTOR_STORE_REGISTRY[store_type]
    return factory_class.create(embedding_model=embedding_model, **kwargs)


def index_documents(documents: list[Document], vector_store, chunkers: list):
    """
    Index documents in the specified vector store using multiple chunking strategies.

    :param documents: List of LangChain Document objects
    :param vector_store: A vector store object
    :param chunkers: List of text splitters to apply
    """
    all_chunks = []

    for chunker in chunkers:
        print(f"🔧 Applying chunker: {chunker.__class__.__name__}")
        chunks = chunker.split_documents(documents)
        print(f"✅ {len(chunks)} chunks created by {chunker.__class__.__name__}")
        all_chunks.extend(chunks)

    print(f"📦 Total {len(all_chunks)} chunks across all strategies. Uploading...")

    vector_store.add_documents(all_chunks)
    print(f"✅ Indexed {len(all_chunks)} chunks.")
