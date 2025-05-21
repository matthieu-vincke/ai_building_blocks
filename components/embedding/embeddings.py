from langchain.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

DEFAULT_MODEL_NAME = "all-mpnet-base-v2"
SUPPORTED_MODELS = {
    "huggingface": HuggingFaceEmbeddings,
    "openai": OpenAIEmbeddings,
}


def get_embedding_model(
    provider: str = "huggingface", model_name: str = DEFAULT_MODEL_NAME
):
    """
    Returns an embedding model instance.

    :param provider: Either "huggingface" or "openai"
    :param model_name: Model identifier (only relevant for HuggingFace)
    :return: Embedding model object
    """
    if provider == "huggingface":
        return HuggingFaceEmbeddings(model_name=f"sentence-transformers/{model_name}")
    elif provider == "openai":
        return OpenAIEmbeddings()
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
