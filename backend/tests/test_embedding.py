from app.services.embedding_service import generate_embeddings

def test_embeddings():
    texts = ["Hello world", "Machine learning is fun"]

    embeddings = generate_embeddings(texts)

    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] > 0