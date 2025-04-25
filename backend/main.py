from fastapi import FastAPI, Query
from typing import List, Optional
import chromadb
from chromadb.utils import embedding_functions
import json
import os
import uvicorn
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cornell Course Search API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB and load data
def initialize_db():
    # Create a client and collection
    client = chromadb.Client()
    
    # Check if collection exists and delete if it does (for development purposes)
    try:
        client.delete_collection("cornell_courses")
    except:
        pass
    
    collection = client.create_collection(
        name="cornell_courses"
    )
    
    # Load course data
    with open('data/fa24.json', 'r') as file:
        courses = json.load(file)
    
    # Load pre-computed embeddings
    with open('data/embeddings/embeddings.json', 'r') as f:
        embeddings = json.load(f)
    
    # Prepare data for ChromaDB
    ids = [str(i) for i in range(len(courses))]
    documents = [f"{course['subject']}: {course['title']} - {course['description']}" for course in courses]
    metadatas = [{"subject": course["subject"], "title": course["title"]} for course in courses]
    embeddings_list = [embeddings[str(i)] for i in range(len(courses))]
    
    # Add data to collection
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings_list
    )
    
    return client, collection

# Initialize database on startup
client, collection = initialize_db()

@app.get("/")
async def root():
    return {"message": "Cornell Course Search API is running"}

@app.get("/api/search")
async def search_courses(
    query: str,
    limit: Optional[int] = Query(10, ge=1, le=100),
    subject_filter: Optional[str] = None
):
    # Apply filters if specified
    where_clause = {}
    if subject_filter:
        where_clause["subject"] = {"$eq": subject_filter}
    
    # Query the collection
    results = collection.query(
        query_texts=[query],
        n_results=limit,
        where=where_clause if where_clause else None
    )
    
    # Format the results
    formatted_results = []
    if results["documents"] and len(results["documents"][0]) > 0:
        for i, (doc, metadata, distance) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            # Extract description from the document
            parts = doc.split(" - ", 1)
            description = parts[1] if len(parts) > 1 else ""
            
            formatted_results.append({
                "id": results["ids"][0][i],
                "subject": metadata["subject"],
                "title": metadata["title"],
                "description": description,
                "relevance_score": 1 - distance  # Convert distance to similarity score
            })
    
    return {"results": formatted_results}

@app.get("/api/subjects")
async def get_subjects():
    # Get unique subject codes from the collection
    all_metadatas = collection.get()["metadatas"]
    unique_subjects = sorted(list(set(item["subject"] for item in all_metadatas)))
    return {"subjects": unique_subjects}

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Check if data file exists
    if not os.path.exists("data/fa24.json"):
        print("Error: data/fa24.json not found. Please add your course data file.")
        exit(1)
    
    # Check if embeddings exist
    if not os.path.exists("data/embeddings/embeddings.json"):
        print("Error: Pre-computed embeddings not found. Please run precompute_embeddings.py first.")
        exit(1)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)