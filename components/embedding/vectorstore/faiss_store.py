from langchain.docstore.in_memory import InMemoryDocstore
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.faiss import FAISS


class FAISSVectorStoreFactory:
    def __init__(self, embedding_model: Embeddings, **kwargs):
        self.embedding_model = embedding_model
        self.index = None
        self.docstore = InMemoryDocstore()
        self.kwargs = kwargs  # Placeholder for extensibility (e.g., save_path)

    def from_documents(self, documents):
        self.index = FAISS.from_documents(
            documents=documents, embedding=self.embedding_model
        )
        return self.index

    def add_documents(self, documents):
        if not self.index:
            self.from_documents(documents)
        else:
            self.index.add_documents(documents)

    def similarity_search(self, query, k=5):
        return self.index.similarity_search(query, k=k)

    def similarity_search_with_score(self, query, k=5):
        return self.index.similarity_search_with_score(query, k=k)

    def save_local(self, path: str):
        if not self.index:
            raise RuntimeError("No FAISS index to save.")
        self.index.save_local(path)

    def load_local(self, path: str):
        self.index = FAISS.load_local(path, embeddings=self.embedding_model)
