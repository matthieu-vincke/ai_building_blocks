# Components Overview

This section provides an overview of the main components in the AI Building Blocks library.

## Embedding Components

The embedding components provide interfaces for working with various embedding models and vector stores.

### Key Features

- Support for multiple embedding providers (OpenAI, HuggingFace, etc.)
- Unified interface for embedding generation
- Integration with popular vector databases

### Example Usage

```python
from components.embedding import get_embedding_model

# Create an OpenAI embedding model
embeddings = get_embedding_model("openai")

# Generate embeddings for text
text_embeddings = embeddings.embed_documents(["Hello world", "AI is amazing"])
```

## Vector Store Components

Vector stores provide efficient storage and retrieval of embeddings.

### Supported Stores

- **FAISS**: Fast in-memory vector search
- **MongoDB Atlas**: Cloud-based vector search with persistence

### Example Usage

```python
from components.embedding.vectorstore import create_vector_store

# Create a MongoDB vector store
vector_store = create_vector_store(
    "mongodb",
    embeddings,
    connection_string="mongodb+srv://...",
    db_name="my_db",
    collection_name="my_collection"
)

# Add documents
vector_store.add_documents(documents)

# Search for similar documents
results = vector_store.similarity_search("query text", k=5)
```

## Web Components

Web components provide utilities for crawling and downloading web content.

### Features

- Deep web crawling with configurable depth
- Content extraction and cleaning
- Support for various file formats

### Example Usage

```python
from components.web import DeepCrawler

# Create a crawler instance
crawler = DeepCrawler(max_depth=2)

# Crawl a website
results = crawler.crawl("https://example.com")
```

## Utility Components

Utility components provide common functionality used across the library.

### Logger

A configured logger for consistent logging across all components.

```python
from components.utils import get_logger

logger = get_logger(__name__)
logger.info("Processing started")
```

## Next Steps

For detailed API documentation, see the [API Reference](source/modules.rst) section.
