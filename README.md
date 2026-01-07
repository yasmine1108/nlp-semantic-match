# nlp-semantic-match
# MLOps Project: Intelligent Equipment Matching API

## Project Overview
This project implements a **Semantic Search Engine** for industrial equipment. It matches unstructured user queries (e.g., "yellow hard hat") to an official product database using **Natural Language Processing (NLP)**.

**Key Features:**
* **Hybrid Retrieval:** Combines Semantic Search (Vector Embeddings) with Lexical Search (Keyword Matching) for maximum accuracy.
* **Model:** Uses `all-MiniLM-L6-v2` with a FAISS Index for high-performance retrieval.
* **MLOps:** Fully Dockerized API with MLflow experiment tracking.
* **Calibration:** Confidence score calibration to filter low-quality matches.

## Project Structure
```bash
├── app/
│   ├── main.py            # FastAPI Application (Logic & Endpoints)
│   └── artifacts/         # Stores the FAISS index and Product Data
├── data/
│   ├── products.csv       # The official equipment database
│   └── test_queries.csv   # Test set for evaluation
├── notebooks/
│   └── experiment.ipynb   # Jupyter Notebook for Training & Evaluation
├── mlruns/                # MLflow local tracking logs
├── Dockerfile             # Instructions to build the container
├── requirements.txt       # Python dependencies
└── README.md
```

## How to Run
### 1. Build the Docker Image (The Backend)
First, we build the container that holds the AI model and API using the command **docker build -t semantic-search-api .**
### 2. Run the API Container
Run the container and map it to port 8000 using the command **docker run -p 8000:80 semantic-search-api**
To verify, you can open your browser to http://localhost:8000/docs. You should see the Swagger UI (an interface provided by FastAPI to test the routes defined in the backend).

### 3. Run the User Interface (The Frontend)
Open a new terminal and run the Streamlit app using the command **streamlit run frontend.py**

### 4. Access the App
Open browser and go to http://localhost:8501

## Evaluation Results
We use a simple sample of official products catalogue dataset and users queries dataset which explains the very good results, obviously with more elaborated datasets the results would be more accurate but regardless the API is effective to match queries to products semantically and lexically.

Recall@1: 1.0 (100%)

Recall@5: 1.0 (100%)

MRR: 1.0

Latency: ~0.02s