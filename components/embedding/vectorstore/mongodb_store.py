import os

from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain_mongodb import MongoDBAtlasVectorSearch


class MongoDBVectorStoreFactory:
    def __init__(
        self,
        embedding_model: Embeddings,
        connection_string: str = None,
        db_name: str = None,
        collection_name: str = None,
        index_name: str = None,
    ):
        self.embedding_model = embedding_model

        # Use environment variables if not explicitly passed
        self.connection_string = connection_string or os.getenv(
            "ATLAS_CONNECTION_STRING"
        )
        self.db_name = db_name or os.getenv("ATLAS_DB")
        self.collection_name = collection_name or os.getenv("ATLAS_COLLECTION")
        self.index_name = index_name or os.getenv("ATLAS_INDEX")

        if not all(
            [
                self.connection_string,
                self.db_name,
                self.collection_name,
                self.index_name,
            ]
        ):
            raise ValueError("Missing MongoDB configuration (env vars or parameters).")

        self.vector_store = MongoDBAtlasVectorSearch.from_connection_string(
            self.connection_string,
            f"{self.db_name}.{self.collection_name}",
            self.embedding_model,
            index_name=self.index_name,
        )

    def from_documents(self, documents: list[Document]):
        """
        Index the documents in MongoDB Atlas using the configured collection and index.
        """
        MongoDBAtlasVectorSearch.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            collection=self.vector_store._collection,
            index_name=self.index_name,
        )

    def similarity_search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, k: int = 5):
        return self.vector_store.similarity_search_with_score(query, k=k)

    def add_documents(self, documents: list[Document]):
        self.vector_store.add_documents(documents)
