import json
import numpy as np
from sentence_transformers import SentenceTransformer
from chromadb import Client, Settings
import os

def precompute_embeddings():
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Using a smaller model
    
    # Create embeddings directory if it doesn't exist
    os.makedirs('data/embeddings', exist_ok=True)
    
    # Load your data
    with open('data/fa24.json', 'r') as f:
        courses = json.load(f)
    
    # Pre-compute embeddings
    embeddings = {}
    for i, course in enumerate(courses):
        # Create the document text in the same format as in main.py
        document = f"{course['subject']}: {course['title']} - {course['description']}"
        embedding = model.encode(document)
        embeddings[str(i)] = embedding.tolist()  # Convert numpy array to list for JSON serialization
    
    # Save embeddings
    with open('data/embeddings/embeddings.json', 'w') as f:
        json.dump(embeddings, f)
    
    print(f"Pre-computed embeddings for {len(embeddings)} documents")

if __name__ == "__main__":
    precompute_embeddings() 