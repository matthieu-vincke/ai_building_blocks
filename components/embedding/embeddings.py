from langchain_community.embeddings import OpenAIEmbeddings
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
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


def bm25_rerank(query, docs, top_k=3):
    """
    Re-ranks documents using BM25 based on keyword overlap.

    :param query: The original query string.
    :param docs: List of (Document, score) tuples from vector search.
    :param top_k: Number of documents to return after re-ranking.
    :return: Re-ranked list of (Document, BM25_score) tuples.
    """
    
    if not docs:
        return []
    
    import nltk
    nltk.download('punkt_tab')

    # Tokenize documents
    tokenized_corpus = [word_tokenize(doc.page_content.lower()) for doc, _ in docs]
    bm25 = BM25Okapi(tokenized_corpus)

    # Tokenize query
    tokenized_query = word_tokenize(query.lower())

    # Score each document
    bm25_scores = bm25.get_scores(tokenized_query)

    # Pair BM25 scores with original documents
    reranked_docs = sorted(
        zip([doc for doc, _ in docs], bm25_scores),
        key=lambda x: x[1],
        reverse=True
    )

    return reranked_docs[:top_k]