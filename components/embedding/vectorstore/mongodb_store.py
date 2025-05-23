import os
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from components.embedding.embeddings import bm25_rerank

class MongoDBVectorStoreFactory:
    """
    A factory for creating and managing a MongoDB vector store with LangChain.

    This class abstracts the connection and operations to a MongoDB collection
    for storing and querying vectorized documents using an embedding model.

    Environment Variables (used if arguments are not passed explicitly):
        - MONGO_CONNECTION_STRING: MongoDB connection URI
        - MONGO_DB: Name of the MongoDB database
        - MONGO_COLLECTION: Name of the collection to use
        - MONGO_INDEX: Name of the vector index in the collection
    """

    def __init__(
        self,
        embedding_model: Embeddings,
        connection_string: str = None,
        db_name: str = None,
        collection_name: str = None,
        index_name: str = None,
    ):
        """
        Initializes the vector store factory with the specified embedding model and
        MongoDB connection details.

        Parameters:
            embedding_model (Embeddings): An instance of a LangChain embedding model.
            connection_string (str, optional): MongoDB connection URI. Defaults to the MONGO_CONNECTION_STRING env var.
            db_name (str, optional): MongoDB database name. Defaults to the MONGO_DB env var.
            collection_name (str, optional): MongoDB collection name. Defaults to the MONGO_COLLECTION env var.
            index_name (str, optional): Name of the vector index. Defaults to the MONGO_INDEX env var.

        Raises:
            ValueError: If any required MongoDB configuration is missing.
        """
        self.embedding_model = embedding_model

        self.connection_string = connection_string or os.getenv("MONGO_CONNECTION_STRING")
        self.db_name = db_name or os.getenv("MONGO_DB")
        self.collection_name = collection_name or os.getenv("MONGO_COLLECTION")
        self.index_name = index_name or os.getenv("MONGO_INDEX")

        if not all([self.connection_string, self.db_name, self.collection_name, self.index_name]):
            raise ValueError("Missing MongoDB configuration (env vars or parameters).")

        self.vector_store = MongoDBAtlasVectorSearch.from_connection_string(
            self.connection_string,
            f"{self.db_name}.{self.collection_name}",
            self.embedding_model,
            index_name=self.index_name,
        )

    def from_documents(self, documents: list[Document]):
        """
        Indexes a list of documents in the MongoDB vector store.

        Parameters:
            documents (list[Document]): A list of LangChain Document objects to be indexed.
        """
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5):
        """
        Performs a similarity search using the vector index.

        Parameters:
            query (str): The text query to search for.
            k (int): The number of top similar documents to return. Defaults to 5.

        Returns:
            List[Document]: A list of matching documents sorted by similarity.
        """
        return self.vector_store.similarity_search(query, k=k)

    def similarity_search_with_score(self, query: str, top_k: int = 5, rerank_with_bm25: bool = True):
        """
        Performs a similarity search and returns results with similarity scores.

        Parameters:
            query (str): The text query to search for.
            top_k (int): The number of top similar documents to return. Defaults to 5.

        Returns:
            List[Tuple[Document, float]]: A list of tuples containing documents and their similarity scores.
        """
        k = top_k
        # Step 1: Perform initial similarity search
        if rerank_with_bm25:
            k = top_k * 2
        results = self.vector_store.similarity_search_with_score(query, k=k)
    
                
        if rerank_with_bm25:
            # Step 2: Re-rank using BM25
            reranked_results = bm25_rerank(query, results, top_k=top_k)
            return reranked_results
        else:
            return results[:top_k]
        

    def add_documents(self, documents: list[Document]):
        """
        Adds new documents to the vector store without re-indexing the entire collection.

        Parameters:
            documents (list[Document]): A list of LangChain Document objects to be added.
        """
        self.vector_store.add_documents(documents)
