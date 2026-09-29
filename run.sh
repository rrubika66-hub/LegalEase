#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "⚖️ Starting LegalEase Backend and Frontend Services..."

# Trap signals to ensure graceful shutdown of both background processes
trap 'echo "Stopping all services..."; kill $(jobs -p) 2>/dev/null || true; exit 0' SIGINT SIGTERM EXIT

# Start FastAPI backend
echo "🚀 Launching FastAPI backend on port 8000..."
uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait briefly for backend startup
sleep 2

# Start Streamlit frontend
echo "💻 Launching Streamlit frontend on port 8501..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 &
FRONTEND_PID=$!

echo "✨ Services are up and running!"
echo "👉 Backend API Docs: http://localhost:8000/docs"
echo "👉 Frontend App:     http://localhost:8501"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
