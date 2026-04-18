import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# CRITICAL: Import the already loaded model from embedding_service
from app.services.embedding_service import model

IMAGE_JSON_PATH = "data/images/images.json"

class ImageStore:
    def __init__(self):
        self.images = []
        self.embeddings = []

    def load_images(self):
        with open(IMAGE_JSON_PATH, "r") as f:
            self.images = json.load(f)

        texts = []
        for img in self.images:
            # Create a rich description for better embedding matching
            text = f"{img['title']} {img['description']} {' '.join(img['keywords'])}"
            texts.append(text)

        # Generate embeddings using the shared model
        self.embeddings = model.encode(texts)

    def find_best_image(self, query):
        # Embed the AI's answer to find the closest matching diagram
        query_embedding = model.encode([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(self.embeddings, query_embedding).flatten()
        
        # Find the index of the highest similarity score
        best_idx = np.argmax(similarities)
        
        return self.images[best_idx]