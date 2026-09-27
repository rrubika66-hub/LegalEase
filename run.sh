#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=========================================================="
echo " Starting LegalEase: AI-Powered Legal Document Generator  "
echo "=========================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating from default template..."
    echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
fi

# Function to handle shutdown of background processes
cleanup() {
    echo ""
    echo "Shutting down LegalEase services..."
    kill $(jobs -p) 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# 1. Start FastAPI Backend API (uvicorn)
echo "Starting FastAPI Backend on http://localhost:8000 ..."
python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait briefly for backend startup
sleep 2

# 2. Start Streamlit Frontend
echo "Starting Streamlit UI on http://localhost:8501 ..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 &
FRONTEND_PID=$!

echo "=========================================================="
echo " LegalEase is live!"
echo " - Frontend: http://localhost:8501"
echo " - API Docs: http://localhost:8000/docs"
echo " Press Ctrl+C to stop all services."
echo "=========================================================="

# Keep script running to maintain child processes
wait
