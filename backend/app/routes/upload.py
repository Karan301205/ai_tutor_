import os
import gc
from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import VectorStore
from app.services import store

router = APIRouter()

UPLOAD_DIR = "data/pdfs"

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # RAG Pipeline
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    # Initialize Vector Store
    store.vector_store = VectorStore(embeddings.shape[1])
    store.vector_store.add(embeddings, chunks)

    # Memory Management: Clear large local variables and trigger GC
    del text
    del embeddings
    gc.collect()

    return {
        "message": "PDF processed successfully",
        "chunks": len(chunks)
    }