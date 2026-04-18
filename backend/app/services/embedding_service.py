from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once (important)
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(text_chunks):
    embeddings = model.encode(text_chunks)
    return np.array(embeddings)