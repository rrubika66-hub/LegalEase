# ⚖️ LegalEase: AI-Powered Legal Document Generator

LegalEase is a full-stack AI platform that automates the generation of legally binding, comprehensive legal documents and agreements using Google Gemini 1.5 Pro.

---

## 🚀 Tech Stack
- **Backend:** FastAPI, Uvicorn, Pydantic, python-dotenv
- **AI Core:** Google Generative AI SDK (`google-generativeai`) using **Gemini 1.5 Pro**
- **Frontend:** Streamlit, Requests
- **Document Exporters:** python-docx, fpdf2, Pillow

---

## 📁 Project Structure

```text
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py      # Gemini 1.5 Pro prompt engineering & client
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                  # FastAPI initialization & CORS
│   └── routes.py                # POST /generate endpoint
├── frontend/
│   └── app.py                   # Streamlit UI, live editor & PDF/DOCX exporters
├── Image/
│   └── logo.png                 # Brand logo & assets
├── .env                         # API keys
├── requirements.txt             # Project dependencies
├── run.sh                       # Startup script for backend & frontend
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rrubika66-hub/LegalEase.git
cd LegalEase
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
Run the startup script:
```bash
bash run.sh
```

Or start the services individually:
- **Backend:** `uvicorn legalEaseAPI.main:app --port 8000 --reload`
- **Frontend:** `streamlit run frontend/app.py --server.port 8501`

---

## 🌐 Access Points
- **Web Interface:** [http://localhost:8501](http://localhost:8501)
- **API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
