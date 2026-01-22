<p align="center">
  <h1 align="center">⚖️ LawGPT</h1>
  <p align="center">
    <strong>Your AI-Powered Gateway to the Indian Constitution</strong>
  </p>
  <p align="center">
    A legal information retrieval system that enables users to search, retrieve, and understand provisions of the Constitution of India through evidence-grounded semantic search.
  </p>
</p>


---

Accessing and understanding legal documents can be challenging for many individuals. LawGPT bridges this gap by providing an intuitive platform that allows users to easily search and comprehend constitutional provisions.

---

## Features

- **Semantic Search** — Find relevant constitutional articles using natural language queries
- **Two-Stage Retrieval** — ColBERT embeddings for initial retrieval + cross-encoder reranking for precision
- **AI-Powered Summaries** — Get concise explanations of constitutional provisions via Gemini

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | [Gradio](https://gradio.app/) |
| **LLM** | [Google Gemini](https://ai.google.dev/) |
| **Vector Database** | [Qdrant](https://qdrant.tech/) |
| **Embeddings** | [FastEmbed](https://qdrant.tech/documentation/fastembed/) (ColBERTv2) |
| **Reranking** | [Jina Reranker v1 Turbo](https://jina.ai/) |
| **Document Store** | [MongoDB](https://www.mongodb.com/) |
| **Package Manager** | [uv](https://docs.astral.sh/uv/) |

---

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- MongoDB instance
- Qdrant instance (local or cloud)

### Environment Setup

1. **Gemini API Key**  
   Sign up at [Google AI Studio](https://aistudio.google.com/apikey) to get your API key and update it in `main.py`.

2. **MongoDB**  
   Update the connection details in [mongodb/database.py](mongodb/database.py):
   ```python
   mongo_client = MongoClient("your-mongodb-connection-string")
   ```

3. **Qdrant**  
   Set up Qdrant locally using Docker or use [Qdrant Cloud](https://cloud.qdrant.io/). Update the connection in [qdrant/embeddings.py](qdrant/embeddings.py):
   ```python
   qdrant_client = QdrantClient(url="your-qdrant-url")
   ```
### Quick Start

```bash
# Clone the repository
git clone https://github.com/abhinav772007/LawGPT.git

# Navigate to project directory
cd LawGPT

# Run the application
uv run main.py
```

Access LawGPT at **http://localhost:7860**

---


---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Query    │────▶│  ColBERT Stage 1 │────▶│   Top 50 Docs   │
└─────────────────┘     │   (FastEmbed)    │     └────────┬────────┘
                        └──────────────────┘              │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  AI Summary     │◀────│  Gemini LLM      │◀────│   Top 10 Docs   │
│  + Citations    │     └──────────────────┘     └────────┬────────┘
└─────────────────┘                                       │
                        ┌──────────────────┐              │
                        │  Jina Reranker   │◀─────────────┘
                        │  (Cross-Encoder) │
                        └──────────────────┘
```

### Why This Stack?

#### Qdrant
A high-performance vector database designed for large-scale datasets with advanced features like similarity search, filtering, and clustering. Efficiently manages and queries constitutional provision embeddings for fast, accurate search results.

#### FastEmbed
A lightweight Python library for embedding generation that integrates seamlessly with Qdrant.

| Benefit | Description |
|---------|-------------|
| **Light** | Minimal dependencies using ONNX runtime — perfect for serverless environments |
| **Fast** | High-performance inference across various hardware platforms |


#### Two-Stage Retrieval
- **Stage 1 (ColBERT)**: Fast multi-vector retrieval to get top 50 candidates
- **Stage 2 (Jina Reranker)**: Cross-encoder reranking for precise top 10 results

---


