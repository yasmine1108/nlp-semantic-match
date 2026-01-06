from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os
import unicodedata
import numpy as np

# --- 1. CONFIGURATION ---
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
THRESHOLD_SEMANTIC = 0.6  # If AI score is below 60%, try keyword search
THRESHOLD_CALIBRATION = 100 # Scaling factor for display

class QueryRequest(BaseModel):
    query: str
    k: int = 3

app = FastAPI(title="Semantic Matching API (Hybrid)", version="2.0")

# --- 2. HELPER FUNCTIONS (Task: Normalization) ---
def normalize_text(text: str) -> str:
    """
    Task: Normalize equipment names (remove noise, accents).
    Example: "Hélmet" -> "helmet"
    """
    if not isinstance(text, str):
        return ""
    # Normalize unicode characters (remove accents)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower().strip()

# --- 3. LOAD ARTIFACTS ---
try:
    print("Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Loading index...")
    index = faiss.read_index(os.path.join(ARTIFACTS_DIR, "faiss_index.bin"))
    
    print("Loading product data...")
    df_products = pd.read_pickle(os.path.join(ARTIFACTS_DIR, "products.pkl"))
    
    # Pre-normalize database names for lexical search later
    df_products['normalized_name'] = df_products['name'].apply(normalize_text)
    
    print("✅ System ready with Hybrid Retrieval!")
except Exception as e:
    print(f"❌ Error loading artifacts: {e}")

@app.post("/match")
def match_products(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # A. Normalize Input
    clean_query = normalize_text(request.query)

    # B. Semantic Search (The "AI" part)
    query_vector = model.encode([request.query])
    faiss.normalize_L2(query_vector)
    D, I = index.search(query_vector, request.k)
    
    results = []
    
    # Process AI Results
    top_score = float(D[0][0])
    
    # C. Hybrid Logic (Task: Semantic + Lexical Fallback)
    # If the AI is unsure (score is low), checks for exact keyword matches
    use_lexical_fallback = top_score < THRESHOLD_SEMANTIC
    
    if use_lexical_fallback:
        print(f"⚠️ Low confidence ({top_score:.2f}). Triggering lexical fallback...")
        # Simple Lexical Search: Does the product name contain the query words?
        # In a real big project, we would use BM25/Elasticsearch, but this is enough for 1.5 weeks.
        lexical_matches = df_products[
            df_products['normalized_name'].str.contains(clean_query, regex=False)
        ]
        
        # If we find exact string matches, prepend them to results
        for _, product in lexical_matches.head(request.k).iterrows():
            results.append({
                "id": int(product['id']),
                "name": product['name'],
                "category": product['category'],
                "score": 1.0, # Exact text match = 100% confidence
                "method": "Lexical Match (Fallback)"
            })
    
    # Add Semantic Results (if not already added by lexical)
    existing_ids = [r['id'] for r in results]
    
    for j, row_index in enumerate(I[0]):
        product = df_products.iloc[row_index]
        p_id = int(product['id'])
        
        if p_id not in existing_ids:
            # D. Calibration (Task: Calibrate scores)
            # Cosine similarity is -1 to 1. We treat it as probability.
            raw_score = float(D[0][j])
            calibrated_score = max(0, raw_score) # Clip negatives
            
            results.append({
                "id": p_id,
                "name": product['name'],
                "category": product['category'],
                "score": round(calibrated_score, 4),
                "method": "Semantic AI"
            })

    # Return top K combined results
    return {
        "query": request.query, 
        "matches": results[:request.k]
    }