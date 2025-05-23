from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import FAISS


class FAISSVectorStoreFactory:
    """
    Factory class for managing a FAISS-based vector store using a specified embedding model.

    This class provides functionality to create, update, search, and persist a FAISS index
    for document embeddings, typically used in semantic search applications.
    """

    def __init__(self, embedding_model: Embeddings, **kwargs):
        """
        Initializes the FAISS vector store factory.

        Parameters:
            embedding_model (Embeddings): An instance of a LangChain embedding model.
            **kwargs: Optional keyword arguments for extensibility (e.g., save path).
        """
        self.embedding_model = embedding_model
        self.index = None
        self.docstore = InMemoryDocstore()
        self.kwargs = kwargs

    def from_documents(self, documents):
        """
        Creates a new FAISS index from a list of documents.

        Parameters:
            documents (list[Document]): A list of LangChain Document objects to be indexed.

        Returns:
            FAISS: The initialized FAISS index.
        """
        self.index = FAISS.from_documents(
            documents=documents, embedding=self.embedding_model
        )
        return self.index

    def add_documents(self, documents):
        """
        Adds new documents to the FAISS index. Initializes the index if it does not exist.

        Parameters:
            documents (list[Document]): A list of LangChain Document objects to add.
        """
        if not self.index:
            self.from_documents(documents)
        else:
            self.index.add_documents(documents)

    def similarity_search(self, query, k=5):
        """
        Performs a similarity search against the indexed documents.

        Parameters:
            query (str): The input text query to search.
            k (int): The number of top similar documents to return. Defaults to 5.

        Returns:
            list[Document]: A list of the most similar documents.
        """
        return self.index.similarity_search(query, k=k)

    def similarity_search_with_score(self, query, k=5):
        """
        Performs a similarity search and returns documents with similarity scores.

        Parameters:
            query (str): The input text query to search.
            k (int): The number of top results to return. Defaults to 5.

        Returns:
            list[tuple[Document, float]]: A list of (document, score) tuples.
        """
        return self.index.similarity_search_with_score(query, k=k)

    def save_local(self, path: str):
        """
        Saves the current FAISS index to the local filesystem.

        Parameters:
            path (str): The directory path where the index should be saved.

        Raises:
            RuntimeError: If the index has not been initialized.
        """
        if not self.index:
            raise RuntimeError("No FAISS index to save.")
        self.index.save_local(path)

    def load_local(self, path: str):
        """
        Loads a FAISS index from the local filesystem.

        Parameters:
            path (str): The directory path from which to load the index.
        """
        self.index = FAISS.load_local(path, embeddings=self.embedding_model)
