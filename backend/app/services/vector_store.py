import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.text_chunks = []

    def add(self, embeddings, chunks):
        self.index.add(embeddings)
        self.text_chunks.extend(chunks)

    def search(self, query_embedding, k=3):
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in indices[0]:
            results.append(self.text_chunks[i])

        return results