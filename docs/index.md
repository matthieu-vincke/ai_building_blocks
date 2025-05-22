# AI Building Blocks Documentation

Welcome to the AI Building Blocks library documentation. This library provides modular components for building AI applications with embeddings, vector stores, web crawling, and more.

## Overview

AI Building Blocks is a collection of reusable components designed to accelerate the development of AI-powered applications. The library includes:

- **Embedding Components**: Tools for creating and managing text embeddings
- **Vector Stores**: Implementations for FAISS and MongoDB Atlas vector storage
- **Web Components**: Web crawling and content downloading utilities
- **Utilities**: Logging and other helper functions

## Quick Start

```python
from components.embedding import get_embedding_model
from components.embedding.vectorstore import create_vector_store

# Create an embedding model
embeddings = get_embedding_model("openai")

# Create a vector store
vector_store = create_vector_store("mongodb", embeddings, connection_string="...")
```

## Contents

```{toctree}
:maxdepth: 2
:caption: User Guide:

components
```

```{toctree}
:maxdepth: 3
:caption: API Reference:

source/modules
```

## Installation

```bash
pip install ai-building-blocks
```

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependencies

## License

This project is licensed under the MIT License.
