from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, chat
from app.services.image_service import ImageStore
from app.services import store
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static/images", StaticFiles(directory="data/images"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_images():
    store.image_store = ImageStore()
    store.image_store.load_images()


app.include_router(upload.router)
app.include_router(chat.router)
