# AI Tutor — RAG-Powered PDF Chatbot
 
An AI-powered tutoring app that lets you upload a PDF (e.g. a textbook chapter) and chat with it. The backend uses a full RAG (Retrieval-Augmented Generation) pipeline with FAISS vector search and Groq LLM, while the frontend is a clean React chat interface with visual aids.
 
---
 
## How It Works
 
1. You upload a PDF → text is extracted, chunked, and embedded using `sentence-transformers`
2. Embeddings are stored in a FAISS vector index
3. When you ask a question → the most relevant chunks are retrieved
4. Groq LLM (LLaMA 3.1) generates an answer from those chunks
5. A relevant image is matched from a local image store and returned alongside the answer
---
 
## Project Structure
 
```
ai-tutor/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routes/
│   │   │   ├── upload.py         # /upload endpoint
│   │   │   └── chat.py           # /chat endpoint
│   │   └── services/
│   │       ├── store.py          # Global state (vector store, image store)
│   │       ├── pdf_service.py    # PDF text extraction (PyMuPDF)
│   │       ├── chunk_service.py  # Text chunking
│   │       ├── embedding_service.py  # Sentence embeddings
│   │       ├── vector_store.py   # FAISS vector search
│   │       ├── llm_service.py    # Groq LLM integration
│   │       └── image_service.py  # Image matching
│   ├── data/
│   │   ├── pdfs/                 # Uploaded PDFs (auto-created)
│   │   └── images/
│   │       ├── images.json       # Image metadata
│   │       └── *.png / *.jpg     # Your image assets
│   ├── tests/
│   │   ├── test_chunk.py
│   │   ├── test_embedding.py
│   │   └── test_pdf.py
│   ├── requirements.txt
│   ├── render.yaml
│   └── run.py
│
└── frontend/
    ├── src/
    │   ├── App.jsx               # Main React component
    │   ├── App.css               # Styles
    │   ├── main.jsx              # React entry point
    │   └── index.css             # Global styles
    ├── public/
    ├── package.json
    └── vite.config.js
```
 
---
 
## Prerequisites
 
Make sure you have the following installed before starting:
 
- **Python** 3.9 or higher → [Download](https://www.python.org/downloads/)
- **Node.js** 18 or higher → [Download](https://nodejs.org/)
- **Git** → [Download](https://git-scm.com/)
- A **Groq API key** → Get one free at [console.groq.com](https://console.groq.com)
---
 
## Local Setup Guide
 
### Step 1 — Clone the Repository
 
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```
 
---
 
### Step 2 — Backend Setup
 
#### 2.1 Navigate to the backend folder
 
```bash
cd backend
```
 
#### 2.2 Create a Python virtual environment
 
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
 
# On Windows
python -m venv venv
venv\Scripts\activate
```
 
> You should see `(venv)` appear at the start of your terminal prompt.
 
#### 2.3 Install dependencies
 
```bash
pip install -r requirements.txt
```
 
>  This may take a few minutes — `sentence-transformers` and `faiss-cpu` are large packages.
 
#### 2.4 Set up environment variables
 
Create a `.env` file in the `backend/` folder:
 
```bash
# On macOS/Linux
touch .env
 
# On Windows
type nul > .env
```
 
Open the `.env` file and add your Groq API key:
 
```env
GROQ_API_KEY=your_groq_api_key_here
```
 
>  Get your free API key at [console.groq.com](https://console.groq.com). Click **API Keys** → **Create API Key**.
 
#### 2.5 Set up the images data
 
The app serves images alongside AI answers. You need to create the images folder and a metadata file:
 
```bash
mkdir -p data/images
```
 
Create `data/images/images.json` with the following structure:
 
```json
[
  {
    "filename": "example.png",
    "title": "Example Diagram",
    "description": "A diagram showing an example concept",
    "keywords": ["example", "concept", "diagram"]
  }
]
```
 
Place your image files (`.png`, `.jpg`) inside `data/images/` and reference them in `images.json`.
 
>  If you don't have images yet, create an empty array `[]` in `images.json` to avoid startup errors. The app will still work — it just won't return images.
 
#### 2.6 Start the backend server
 
```bash
python run.py
```
 
You should see output like:
 
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```
 
> The backend runs on **http://127.0.0.1:8000** by default.
 
#### 2.7 Verify the backend is running
 
Open your browser and visit:
 
```
http://127.0.0.1:8000/docs
```
 
You should see the FastAPI interactive API docs (Swagger UI).
 
---
 
### Step 3 — Frontend Setup
 
Open a **new terminal window** (keep the backend running).
 
#### 3.1 Navigate to the frontend folder
 
```bash
cd frontend
```
 
#### 3.2 Install dependencies
 
```bash
npm install
```
 
#### 3.3 Set up environment variables
 
Create a `.env` file in the `frontend/` folder:
 
```bash
# On macOS/Linux
touch .env
 
# On Windows
type nul > .env
```
 
Add the following to the `.env` file:
 
```env
VITE_API_URL=http://127.0.0.1:8000
```
 
#### 3.4 Start the frontend dev server
 
```bash
npm run dev
```
 
You should see:
 
```
  VITE v5.x.x  ready in xxx ms
 
  ➜  Local:   http://localhost:5173/
```
 
#### 3.5 Open the app
 
Visit **http://localhost:5173** in your browser. You should see the AI Tutor landing page.
 
---
 
##  Running Tests
 
Make sure you're in the `backend/` folder with your virtual environment activated.
 
```bash
# Run all tests
pytest
 
# Run a specific test file
pytest tests/test_pdf.py
pytest tests/test_embedding.py
pytest tests/test_chunk.py
 
# Run with verbose output
pytest -v
```
 
---
 
##  Using the App
 
1. Open **http://localhost:5173**
2. Click the upload area and select a PDF file (e.g. a textbook chapter)
3. Wait for the PDF to be processed (you'll be taken to the chat view automatically)
4. Type any question related to the PDF content and press **Enter** or click the send button
5. The AI will answer using only the content from your PDF, with a relevant image if available
6. Click **New Chapter** in the header to upload a different PDF
---
 
##  Common Issues & Fixes
 
**`ModuleNotFoundError` when starting the backend**
> Make sure your virtual environment is activated (`source venv/bin/activate` on Mac/Linux or `venv\Scripts\activate` on Windows) and you've run `pip install -r requirements.txt`.
 
**`GROQ_API_KEY not found` error**
> Double-check your `.env` file is inside the `backend/` folder (not the project root) and contains `GROQ_API_KEY=your_key_here` with no spaces around the `=`.
 
**`FileNotFoundError: data/images/images.json`**
> Create the `data/images/` directory and add an `images.json` file. See Step 2.5 above.
 
**CORS error in the browser console**
> Make sure the backend is running on port `8000` and the `VITE_API_URL` in your frontend `.env` matches exactly: `http://127.0.0.1:8000`.
 
**Frontend shows blank page**
> Run `npm install` again and make sure you're using Node.js 18+. Check the terminal for any error messages.
 
**PDF upload hangs**
> Large PDFs can take time to process due to embedding generation. Try with a smaller PDF first (under 50 pages).
 
---
 
##  Environment Variables Summary
 
| Variable | Location | Description |
|---|---|---|
| `GROQ_API_KEY` | `backend/.env` | Your Groq API key for LLM access |
| `VITE_API_URL` | `frontend/.env` | Backend URL (local or deployed) |
 
---
 
##  Tech Stack
 
| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI + Uvicorn |
| PDF Parsing | PyMuPDF (fitz) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Search | FAISS |
| LLM | Groq (LLaMA 3.1 8B) |
| Image Matching | scikit-learn cosine similarity |
 
---
 
