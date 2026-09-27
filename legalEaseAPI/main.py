import os
import sys

# Ensure parent directory is in sys.path when running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from legalEaseAPI.routes import router as document_router

app = FastAPI(
    title="LegalEase AI Legal Document Generator",
    description="High-performance backend API powering automated, production-grade legal document generation using Gemini 1.5 Pro.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local Streamlit frontend and other clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Document Generation API router
app.include_router(document_router)

@app.get("/", tags=["Health Check"])
async def root_health_check():
    """
    Health check and welcome endpoint.
    """
    return {
        "status": "online",
        "service": "LegalEase AI Legal Document Generator",
        "version": "1.0.0",
        "message": "Welcome to the LegalEase API. Visit /docs for interactive API documentation.",
    }

if __name__ == "__main__":
    uvicorn.run("legalEaseAPI.main:app", host="0.0.0.0", port=8000, reload=True)
