import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from legalEaseAPI.routes import router

# Initialize FastAPI App
app = FastAPI(
    title="LegalEase AI Legal Document Generator",
    description="Production-ready FastAPI backend powered by Gemini 1.5 Pro to generate legally binding documents.",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Document Generation Router
app.include_router(router)

@app.get("/", tags=["Health Check"])
async def root():
    """
    Health check and welcome endpoint.
    """
    return {
        "message": "Welcome to LegalEase AI Legal Document Generator API",
        "status": "active",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("legalEaseAPI.main:app", host="0.0.0.0", port=8000, reload=True)
