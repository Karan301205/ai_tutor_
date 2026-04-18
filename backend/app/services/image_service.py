import json
import numpy as np
# Remove the local SentenceTransformer import to save memory
from sklearn.metrics.pairwise import cosine_similarity
# Import the existing model instance from your embedding service
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
            # Combining metadata for better search matching
            text = f"{img['title']} {img['description']} {' '.join(img['keywords'])}"
            texts.append(text)

        # Use the shared model instance instead of a new one
        self.embeddings = model.encode(texts)

    def find_best_image(self, query):
        # Generate embedding for the AI's answer
        query_embedding = model.encode([query])

        # Calculate similarity between the answer and image metadata
        similarities = cosine_similarity(self.embeddings, query_embedding).flatten()

        # Pick the image with the highest similarity score
        best_idx = np.argmax(similarities)

        return self.images[best_idx]