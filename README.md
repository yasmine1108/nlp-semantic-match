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
├── .dvc/                      
├── .github/
│   └── workflows/
│       └── ci.yml             
├── app/
│   ├── main.py                # Backend Service (FastAPI)
│   └── artifacts/             
├── data/
│   ├── products.csv.dvc       
│   ├── test_queries.csv.dvc  
│   ├── .gitignore    
│   ├── test_queries.csv      
│   └── products.csv         
├── notebooks/
│   └── experiment.ipynb       # Experimentation & Evaluation
├── venv/
├── generate_data.py           # Script to generate synthetic catalogue
├── docker-compose.yml         # Orchestrates Backend + Frontend containers
├── Dockerfile                 
├── requirements.txt           
├── frontend.py
├── test_normalization.py
├── .dockerignore
├── .dvcignore
├── dvc-key.json
├── .gitignore                 
└── README.md
```

## How to Run

### 1. Run the docker-compose file
Run the docker-compose.yml file using the command **docker-compose up**.

After the image is built, you will be presented with two containers: one for the backend and one for the frontend.

The backend runs on the port **http://localhost:8000** and you can access to **http://localhost:8000/docs** to see the Swager UI (an interface provided by FastAPI to test the routes defined in the backend).
The frontend can be accessed via the url **http://localhost:8501**.

Open the browser and go to the url that best fits you to use and test the application.

## Evaluation Results
We use a simple sample of official products catalogue dataset and users queries dataset which explains the very good results, obviously with more elaborated datasets the results would be more accurate but regardless the API is effective to match queries to products semantically and lexically.