from .faiss_store import FAISSVectorStoreFactory
from .mongodb_store import MongoDBVectorStoreFactory


def create_vector_store(store_type: str, embedding_model, **kwargs):
    if store_type == "mongodb":
        return MongoDBVectorStoreFactory(embedding_model, **kwargs)
    elif store_type == "faiss":
        return FAISSVectorStoreFactory(embedding_model, **kwargs)
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")
