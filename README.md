# 🔎 Semantic Search Engine

A lightweight semantic document retrieval system that searches documents based on **meaning rather than exact keyword matching**.

The project uses **Sentence Transformers** to convert document chunks and queries into embeddings, **ChromaDB** for vector similarity search, **FastAPI** as the backend API, and **Streamlit** as the interactive frontend.

The system also includes a small retrieval evaluation framework to compare different document chunking strategies using **Precision@5**.

---

## ✨ Features

* 🔎 Semantic search using sentence embeddings
* 🧠 `all-MiniLM-L6-v2` embedding model
* 🗂️ Automatic document loading from `.txt` files
* ✂️ Paragraph-based and fixed-size chunking
* 🗄️ Persistent ChromaDB vector storage
* ⚡ FastAPI `/search` REST endpoint
* 🖥️ Streamlit web interface
* 📊 Precision@5 retrieval evaluation
* 🧪 Automated tests using pytest
* 💻 Runs locally without a GPU or paid API
* 🔌 Configurable Top-K search results

---

## 🏗️ Architecture

```text
                         Documents
                             │
                             ▼
                         Chunking
                             │
                  ┌──────────┴──────────┐
                  │                     │
            Paragraph-based       Fixed-size
                  │                     │
                  └──────────┬──────────┘
                             │
                             ▼
                    Sentence Transformer
                     all-MiniLM-L6-v2
                             │
                             ▼
                        Embeddings
                             │
                             ▼
                         ChromaDB
                             │
                       Vector Search
                             │
                             ▼
                         FastAPI
                         /search
                             │
                             ▼
                        Streamlit UI
                             │
                             ▼
                     Ranked Results
```

---

## 🧠 How It Works

### 1. Document Loading

The system reads `.txt` files from the `documents/` directory.

Example:

```text
documents/
├── python.txt
├── machine_learning.txt
└── database.txt
```

Each document is stored together with its filename so that search results can identify their source.

---

### 2. Document Chunking

Large documents are divided into smaller pieces before generating embeddings.

Two approaches were implemented:

#### Paragraph-based chunking

Each paragraph becomes a separate chunk.

Advantages:

* Preserves natural semantic boundaries
* Keeps related sentences together
* Simple to implement

#### Fixed-size chunking

Documents are split into chunks containing approximately 40 words.

This provides more consistent chunk sizes but can sometimes split an idea or sentence across two chunks.

Both strategies were evaluated rather than assuming one approach would always perform better.

---

### 3. Embedding Generation

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The model generates **384-dimensional embeddings**.

Semantically similar text produces vectors that are closer together in the embedding space.

For example:

```text
"What is SQL used for?"
```

can retrieve a chunk discussing:

```text
"SQL is used to create, read, update, and delete data..."
```

even when the wording is not exactly the same.

---

### 4. Vector Storage

The embeddings are stored locally using **ChromaDB**.

The database stores:

* Chunk ID
* Chunk text
* Embedding vector
* Source filename metadata

The project maintains separate collections for the two chunking experiments:

```text
documents
fixed_documents
```

---

### 5. Semantic Search

When a user enters a query:

```text
What algorithms are used for supervised learning?
```

the query is converted into an embedding using the same model.

ChromaDB then compares the query embedding against stored document embeddings and returns the most similar chunks.

The API returns:

* Rank
* Source filename
* Retrieved text
* Vector distance

A smaller distance indicates greater similarity for the configured ChromaDB distance metric.

---

## 🔌 FastAPI Backend

The retrieval system is exposed through a REST API.

### Endpoint

```text
POST /search
```

### Request

```json
{
  "query": "What is SQL used for?",
  "top_k": 5
}
```

### Response

```json
{
  "query": "What is SQL used for?",
  "results": [
    {
      "rank": 1,
      "source": "database.txt",
      "text": "SQL is used to create, read, update, and delete data in relational databases.",
      "distance": 0.123
    }
  ]
}
```

FastAPI also provides automatically generated interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## 🖥️ Streamlit Interface

A Streamlit frontend provides a simple interface for interacting with the search API.

The application allows users to:

* Enter natural-language queries
* Select the number of results
* View retrieved document chunks
* See source filenames
* Inspect retrieval distances
* View the embedding model and system configuration
* View retrieval evaluation results

The frontend communicates with the FastAPI backend over HTTP.

```text
Streamlit
    │
    │ HTTP POST
    ▼
FastAPI /search
    │
    ▼
Semantic Retrieval
    │
    ▼
ChromaDB
```

---

## 📊 Retrieval Evaluation

A labelled evaluation set containing **10 queries** was created.

Each query has an expected source document.

The system uses:

### Precision@5

Precision@5 measures how many of the top five retrieved results belong to the expected source document.

```text
Precision@5 =
Relevant results in top 5
-------------------------
           5
```

### Results

| Chunking Strategy     | Chunks | Precision@5 |
| --------------------- | -----: | ----------: |
| Paragraph-based       |      8 |    **0.54** |
| Fixed-size (40 words) |      6 |    **0.54** |

The two approaches produced the same Precision@5 on the current evaluation dataset.

Because the evaluation dataset is intentionally small, these results should be treated as a **baseline experiment rather than a general benchmark**.

---

## 🧪 Testing

The project includes automated tests using `pytest`.

Current tests verify:

* Search returns the expected response fields
* Relevant documents can be retrieved
* The `top_k` parameter is respected

Run the tests with:

```bash
pytest
```

Expected result:

```text
3 passed
```

---

## 🛠️ Tech Stack

| Technology            | Purpose                              |
| --------------------- | ------------------------------------ |
| Python                | Core implementation                  |
| Sentence Transformers | Text embeddings                      |
| all-MiniLM-L6-v2      | Embedding model                      |
| ChromaDB              | Vector storage and similarity search |
| FastAPI               | REST API backend                     |
| Streamlit             | Interactive frontend                 |
| Pydantic              | API request validation               |
| Requests              | Streamlit → FastAPI communication    |
| Pytest                | Automated testing                    |

---

## 📁 Project Structure

```text
Semantic_Search/
│
├── app/
│   ├── __init__.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── search.py
│   ├── main.py
│   ├── fixed_chunker.py
│   ├── fixed_vector_store.py
│   ├── evaluation_data.py
│   ├── evaluate.py
│   ├── evaluate_fixed.py
│   └── test_search.py
│
├── documents/
│   ├── python.txt
│   ├── machine_learning.txt
│   └── database.txt
│
├── chroma_db/
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/donna2864/Semantic-Search.git
cd Semantic_Search
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Step 1 — Build the vector database

Run:

```bash
python app/vector_store.py
```

This loads the documents, creates embeddings, and stores them in ChromaDB.

---

### Step 2 — Start FastAPI

Open a terminal:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Step 3 — Start Streamlit

Open a second terminal and activate the virtual environment.

Run:

```bash
streamlit run streamlit_app.py
```

The Streamlit application will open in your browser.

---

## 🔍 Example Queries

Try queries such as:

```text
What programming language is known for simple syntax?
```

```text
What algorithms are used for supervised learning?
```

```text
How do computers learn patterns from data?
```

```text
What is a relational database?
```

```text
What is SQL used for?
```

```text
What are some examples of NoSQL databases?
```

---

## 🔮 Future Improvements

Possible extensions include:

* Support for PDF and DOCX documents
* Configurable chunk size and overlap
* Hybrid keyword + semantic search
* Metadata filtering
* Larger evaluation datasets
* Recall@K and Mean Reciprocal Rank evaluation
* Search result highlighting
* Batch document ingestion
* Dockerized deployment
* RAG-based answer generation on top of the retrieval layer

---

## 📌 Project Scope

This project focuses specifically on **semantic information retrieval**.

It does not generate answers using an LLM. The system retrieves relevant document chunks and returns them to the user.

This separation makes the project suitable as a retrieval component that could later be integrated into a **Retrieval-Augmented Generation (RAG)** pipeline.

---

## 👩‍💻 Author

**Donna R**

BSc (Hons) Computer Science
RV University, Bengaluru

---