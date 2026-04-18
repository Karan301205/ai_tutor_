from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import model
from app.services.llm_service import generate_answer
from app.services import store

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatRequest):
    if store.vector_store is None:
        return {"error": "No document uploaded yet"}

    try:
        query_embedding = model.encode([req.question])
        query_embedding = query_embedding.reshape(1, -1)

        relevant_chunks = store.vector_store.search(query_embedding, k=3)

        answer = generate_answer(req.question, relevant_chunks)
        image = store.image_store.find_best_image(answer)

        return {
            "answer": answer,
            "image": {
                "filename": image["filename"],
                "title": image["title"]
            }
        }

    except Exception as e:
        return {"error": str(e)}