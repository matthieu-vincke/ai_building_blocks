# ai_building_blocks
Building Blocks for AI Applications

pre-commit install

Local Machine

make venv PYTHON_BIN="C:/Softs/Py310_64/python.exe"
make install


ai-building-blocks/
│
├── components/
    ├── embedding/
    │   ├── encoder.py         # Convert text/data to embeddings using models
    │   ├── vector_store.py    # Interface with vector DBs (FAISS, Pinecone, Chroma, etc.)
    │   └── pipeline.py        # End-to-end pipeline: from text → embeddings → vector DB
    ├── web/
    │   ├── crawler.py        # handles website crawling, pagination, robots.txt
    │   ├── extractor.py      # parsing HTML, extracting structured data
    │   └── cleaner.py        # optional: clean or normalize scraped content
│   ├── data/
│   │   ├── loaders.py
│   │   ├── preprocessors.py
│   ├── models/
│   │   ├── base_model.py
│   │   ├── mlp.py
│   ├── training/
│   │   ├── trainer.py
│   │   ├── scheduler.py
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── visualizations.py
│   └── utils/
│       ├── logger.py
│       ├── config.py
│
├── examples/
│   ├── classification/
│   │   └── train_mlp.py
│   ├── regression/
│       └── train_regression.py
│
├── tests/
│   ├── test_models.py
│   ├── test_data.py
│
├── scripts/
│   ├── download_data.py
│   └── convert_model.py
│
├── docs/
│   └── README.md
│
├── .gitignore
├── requirements.txt
├── setup.py
├── README.md
└── pyproject.toml (optional, for modern Python packaging)
