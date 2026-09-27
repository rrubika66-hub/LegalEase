@echo off
echo ==========================================================
echo  Starting LegalEase: AI-Powered Legal Document Generator
echo ==========================================================

REM Start FastAPI Backend
start "LegalEase Backend API" cmd /k "python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM Start Streamlit Frontend
start "LegalEase Streamlit UI" cmd /k "streamlit run frontend/app.py --server.port 8501"

echo ==========================================================
echo  LegalEase services launched in separate windows!
echo  - Frontend: http://localhost:8501
echo  - Backend Docs: http://localhost:8000/docs
echo ==========================================================
