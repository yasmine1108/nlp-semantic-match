import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:8000/match"  # Where your API lives

st.set_page_config(page_title="Industrial Search Tool", page_icon="🔧")

# --- UI Header ---
st.title("🔧 Smart Equipment Search")
st.markdown("Find the right part using **semantic descriptions** (e.g., 'yellow hard hat').")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Search Settings")
    k_neighbors = st.slider("Number of Results", min_value=1, max_value=10, value=3)

# --- Main Search Input ---
query = st.text_input("Describe the equipment you need:", placeholder="Type here...")
search_button = st.button("🔍 Search Database")

# --- Logic ---
if search_button and query:
    with st.spinner("Searching AI Database..."):
        try:
            # Send request to your FastAPI backend
            payload = {"query": query, "k": k_neighbors}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("matches", [])
                
                if not results:
                    st.warning("No matches found.")
                else:
                    st.success(f"Found {len(results)} matches!")
                    
                    # Display results neatly
                    for item in results:
                        # Color code based on score
                        score = item['score']
                        color = "green" if score > 0.8 else "orange" if score > 0.5 else "red"
                        
                        with st.container():
                            st.markdown(f"### {item['name']}")
                            st.caption(f"Category: {item['category']} | ID: {item['id']}")
                            st.markdown(f"**Confidence:** :{color}[{score:.4f}]")
                            st.divider()
            else:
                st.error(f"Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🚨 Could not connect to the API. Is the Docker container running?")