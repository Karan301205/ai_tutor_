import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('all-MiniLM-L6-v2')

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
            text = (
                img["title"] + " " +
                img["description"] + " " +
                " ".join(img["keywords"])
            )
            texts.append(text)

        self.embeddings = model.encode(texts)

    def find_best_image(self, query):
        query_embedding = model.encode([query])

        similarities = cosine_similarity(self.embeddings, query_embedding).flatten()

        best_idx = np.argmax(similarities)

        return self.images[best_idx]