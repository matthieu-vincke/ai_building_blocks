# 🧠 AI Building Blocks

Modular, testable components to accelerate the development of AI applications in Python.

Docs: https://matthieu-vincke.github.io/ai_building_blocks/

## 📂 Project Structure

```
ai_building_blocks/
│
├── components/
│   ├── web/
│   │   └── downloader.py         # Functions to crawl and download documents
│   ├── embedding/
│   │   └── embedder.py           # Embeds text and stores in vector DB
│   └── utils/
│       └── logger.py             # Standardized logger
│
├── tests/
│   ├── web/
│   │   └── test_downloader.py
│   └── embedding/
│       └── test_embedder.py
│
├── requirements.txt
├── requirements-dev.txt
├── Makefile
└── README.md
```

## 🚀 Features

- 📄 **Web Crawling & Document Downloading**: HTML-based file extraction
- 🧠 **Text Embedding**: Convert text to vector representations
- 🗃️ **Vector Storage**: (Pluggable) vector DB integration
- 🛠️ **Utilities**: Logging, formatting, testing
- ✅ **Test Coverage**: With `pytest` and mocking
- ⚙️ **Cross-platform Build System**: `make` support (with Windows compatibility)

## 🔧 Setup

```bash
PYTHONPATH=.
```

1. **Create and activate virtual environment**
```bash
make venv PYTHON_BIN=/path/to/python
```

2. **Install dependencies**
```bash
make dev-install
```

3. **Run checks**
```bash
make check
```

## 🧪 Testing

```bash
make test
```

## 📦 Dependencies

Main requirements in `requirements.txt`:

- `requests`
- `beautifulsoup4`
- `openai` or other embedding providers
- `chromadb` (optional for vector DB)

Dev/test in `requirements-dev.txt`:

- `pytest`
- `pytest-mock`
- `flake8`
- `black`
- `isort`
- `pre-commit`

## ✍️ Logging

Uses `utils.logger` to ensure consistent logging throughout modules.

```python
from utils.logger import get_logger
logger = get_logger(__name__)
logger.info("Hello from logger!")
```

## 📘 Example Usage

```python
from components.web.downloader import download_documents_from_html
from components.embedding.embedder import embed_texts

html = "<html>...</html>"
download_documents_from_html(html, base_url="https://example.com", download_folder="./data")

embeddings = embed_texts(["Document content here"], embedding_model="openai", persist=True)
```

## 🔒 Code Quality with Pre-commit

To automatically enforce code formatting and linting before each commit, this project supports `pre-commit` hooks.

### 🔧 Setup

```bash
# Install pre-commit if not already installed
pip install pre-commit

# Install the hooks defined in .pre-commit-config.yaml
pre-commit install
```

Now, every time you commit, tools like `black` and `isort` will run automatically.

To manually run all hooks on all files:
```bash
pre-commit run --all-files
```

## ✅ TODO

- [ ] Add support for LangChain or HuggingFace embeddings
- [ ] Add command-line interface
- [ ] Extend vector DB support (e.g. Pinecone, Weaviate)

## 📄 License

MIT License
