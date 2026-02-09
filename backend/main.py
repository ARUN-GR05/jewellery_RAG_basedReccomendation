from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.search import SearchEngine
from src.ocr import extract_text
from src.vision import analyze_image_with_text

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine
search_engine = SearchEngine()

@app.get("/ping")
async def ping():
    """
    Lightweight health check endpoint to wake up the server.
    """
    return {"status": "ok"}

@app.post("/search")
async def text_search(query: str = Form(...), top_k: int = Form(5)):
    """
    Text-based semantic search endpoint.
    """
    try:
        results = search_engine.search(query, top_k=top_k)
        return {"results": results}
    except Exception as e:
        print(f"Error in /search: {e}")
        return {"error": str(e), "results": []}

@app.post("/analyze")
async def image_analyze(file: UploadFile = File(...), top_k: int = Form(5)):
    """
    Image analysis endpoint: OCR + Vision → Search.
    """
    try:
        # Load image
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        
        # Step 1: OCR
        ocr_text = extract_text(image)
        
        # Step 2: Vision Analysis
        vision_description = analyze_image_with_text(image, ocr_text)
        
        # Step 3: Search using vision description
        results = search_engine.search(vision_description, top_k=top_k)
        
        return {
            "ocr_text": ocr_text,
            "analysis": vision_description,
            "results": results
        }
    except Exception as e:
        print(f"Error in /analyze: {e}")
        return {
            "error": str(e),
            "ocr_text": "",
            "analysis": "Error processing image",
            "results": []
        }

# Serve frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
