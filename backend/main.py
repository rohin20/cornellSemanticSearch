from fastapi import FastAPI, Query
from typing import List, Optional
import chromadb
from chromadb.utils import embedding_functions
import json
import os
import uvicorn
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cornell Course Search API")

# Log all registered routes on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    for route in app.routes:
        logger.info(f"Registered route: {route.path}")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add middleware to log CORS headers
@app.middleware("http")
async def log_headers(request, call_next):
    response = await call_next(request)
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Response headers: {response.headers}")
    return response

# Initialize ChromaDB and load data
def initialize_db():
    try:
        # Log current working directory and file paths
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Data directory contents: {os.listdir('data') if os.path.exists('data') else 'data directory not found'}")
        logger.info(f"Embeddings directory contents: {os.listdir('data/embeddings') if os.path.exists('data/embeddings') else 'embeddings directory not found'}")
        
        # Create a client and collection
        client = chromadb.Client()
        logger.info("Created ChromaDB client")
        
        # Check if collection exists and delete if it does (for development purposes)
        try:
            client.delete_collection("cornell_courses")
            logger.info("Deleted existing collection")
        except:
            logger.info("No existing collection to delete")
        
        collection = client.create_collection(
            name="cornell_courses"
        )
        logger.info("Created new collection")
        
        # Load course data
        try:
            with open('data/fa24.json', 'r') as file:
                courses = json.load(file)
            logger.info(f"Loaded {len(courses)} courses")
        except Exception as e:
            logger.error(f"Error loading course data: {str(e)}")
            raise
        
        # Load pre-computed embeddings
        try:
            with open('data/embeddings/embeddings.json', 'r') as f:
                embeddings = json.load(f)
            logger.info(f"Loaded {len(embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Error loading embeddings: {str(e)}")
            raise
        
        # Prepare data for ChromaDB
        ids = [str(i) for i in range(len(courses))]
        documents = [f"{course['subject']}: {course['title']} - {course['description']}" for course in courses]
        metadatas = [{"subject": course["subject"], "title": course["title"]} for course in courses]
        embeddings_list = [embeddings[str(i)] for i in range(len(courses))]
        
        # Add data to collection
        try:
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings_list
            )
            logger.info("Added data to collection")
        except Exception as e:
            logger.error(f"Error adding data to collection: {str(e)}")
            raise
        
        return client, collection
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

# Initialize database on startup
try:
    client, collection = initialize_db()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise

@app.get("/")
async def root():
    return {"message": "Cornell Course Search API is running"}

@app.get("/search")
async def search_courses(
    query: str,
    limit: Optional[int] = Query(10, ge=1, le=100),
    subject_filter: Optional[str] = None
):
    try:
        logger.info(f"Search request received: query='{query}', limit={limit}, subject_filter={subject_filter}")
        
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
        logger.info(f"Query returned {len(results['documents'][0]) if results['documents'] else 0} results")
        
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
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        raise

@app.get("/subjects")
async def get_subjects():
    try:
        # Get unique subject codes from the collection
        all_metadatas = collection.get()["metadatas"]
        unique_subjects = sorted(list(set(item["subject"] for item in all_metadatas)))
        logger.info(f"Returning {len(unique_subjects)} unique subjects")
        return {"subjects": unique_subjects}
    except Exception as e:
        logger.error(f"Error in subjects endpoint: {str(e)}")
        raise

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Check if data file exists
    if not os.path.exists("data/fa24.json"):
        logger.error("Error: data/fa24.json not found. Please add your course data file.")
        exit(1)
    
    # Check if embeddings exist
    if not os.path.exists("data/embeddings/embeddings.json"):
        logger.error("Error: Pre-computed embeddings not found. Please run precompute_embeddings.py first.")
        exit(1)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)