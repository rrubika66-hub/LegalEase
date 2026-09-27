# ⚖️ LegalEase: AI-Powered Legal Document Generator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Pro-8E75B2.svg)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LegalEase** is a production-grade, AI-driven legal agreement generator designed to draft comprehensive, jurisdiction-compliant contracts in seconds. Leveraging **Google Gemini 1.5 Pro**, an asynchronous **FastAPI** backend, and an interactive **Streamlit** user interface, LegalEase translates conversational covenants into binding legal documents with multi-format export capabilities (`.txt`, `.docx`, and `.pdf`).

---

## 🌟 Key Features

- **Gemini 1.5 Pro AI Engine**: Uses low-temperature prompt engineering (`temperature=0.2`) to draft structured 8-tier contracts with zero conversational fluff.
- **Decoupled Architecture**: High-speed, asynchronous REST API with Pydantic schema validation and CORS support.
- **Live In-Browser Editing**: Streamlit interface allows users to review, edit, and tailor generated legal text before export.
- **Multi-Format Headless Exporters**:
  - 📄 **Plain Text (.txt)**: Clean UTF-8 text formatting.
  - 📘 **Word Document (.docx)**: Times New Roman typography, 1-inch margins, and hierarchical headings via `python-docx`.
  - 📕 **Adobe PDF (.pdf)**: Automatic Unicode sanitization (prevents Latin-1 encoding errors), header/footer numbering, and page breaks via `fpdf2`.
- **Pre-Built Scenario Presets**: Tested across Employment Agreements, Mutual NDAs, and Residential Leases.

---

## 🏛️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   |                        Streamlit Web UI (Port 8501)                       |   |
|   |   - Interactive Input Form: Parties, Covenants, Dates, Document Type      |   |
|   |   - Real-time Markdown Preview & In-browser Text Editor                   |   |
|   |   - Instant Exporters: [.TXT] [.DOCX] [.PDF]                              |   |
|   +-------------------------------------+-------------------------------------+   |
+-----------------------------------------|-----------------------------------------+
                                          | HTTP POST {"document_type", "parties", ...}
                                          v
+-----------------------------------------------------------------------------------+
|                                  BACKEND API LAYER                                |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   |                        FastAPI Server (Uvicorn Port 8000)                 |   |
|   |   - Pydantic Schema Validation (DocumentRequest)                          |   |
|   |   - Cross-Origin Resource Sharing (CORS) Middleware                       |   |
|   |   - Interactive Swagger Docs at /docs & Redoc at /redoc                   |   |
|   +-------------------------------------+-------------------------------------+   |
+-----------------------------------------|-----------------------------------------+
                                          | Method Call: generate_document()
                                          v
+-----------------------------------------------------------------------------------+
|                                  AI CORE LAYER                                    |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   |                        GeminiDocumentGenerator                            |   |
|   |   - Google Generative AI SDK (gemini-1.5-pro)                             |   |
|   |   - Prompt Structure: Preamble -> Terms -> Clauses -> Signatures          |   |
|   |   - Generation Settings: Temperature 0.2, Max Tokens 8192                 |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Directory
```bash
git clone https://github.com/yourusername/LegalEase.git
cd LegalEase
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Branding Assets
```bash
python Image/generate_logo.py
```

### 5. Launch Application

#### On Windows (Single Command):
```cmd
run.bat
```

#### On Linux / macOS / Git Bash:
```bash
bash run.sh
```

#### Or Launch Manually:
```bash
# Terminal 1: Backend API
python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Streamlit Frontend
streamlit run frontend/app.py --server.port 8501
```

- **Frontend UI**: [http://localhost:8501](http://localhost:8501)
- **Interactive API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 REST API Documentation

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Root health-check and service status | `200 OK` |
| `POST` | `/generate` | Generates a complete legal contract | `200 OK`, `422 Unprocessable`, `500 Error` |
| `GET` | `/docs` | Interactive Swagger UI API documentation | `200 OK` |
| `GET` | `/redoc` | Redoc formatted API documentation | `200 OK` |

### Sample Request Payload (`POST /generate`):
```json
{
  "document_type": "Freelance Software Development Agreement",
  "parties": "Client: Alpha Global Inc. (Delaware); Contractor: Alex Morgan (Independent Engineer)",
  "terms": "Full-stack web application development; $15,000 total fee in 3 milestones; Full IP assignment upon payment; 2-year confidentiality; Governing law Delaware",
  "dates": "Effective Date: October 1, 2026; Due Date: December 31, 2026"
}
```

---

## 🧪 Automated Testing Suite

LegalEase includes an end-to-end headless automated test suite covering all core scenarios:

```bash
python test_all_scenarios.py
```

### Verified Scenarios:
1. **Startup Executive Employment Agreement** (Salary, 4-year equity vesting with 1-year cliff, IP assignment, non-solicitation).
2. **Freelancer Non-Disclosure Agreement (NDA)** (2-year confidentiality, trade secret protection, injunctive relief).
3. **Residential Lease Agreement** (Monthly rent, escrow security deposit, maintenance, landlord/tenant statute compliance).

Generated output files are automatically saved to [`exports/`](file:///C:/Users/ELCOT/.gemini/antigravity-ide/scratch/LegalEase/exports/) in `.txt`, `.docx`, and `.pdf` formats.

---

## 📂 Project Directory Structure

```
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py     # Gemini 1.5 Pro AI drafting engine
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry-point
│   └── routes.py               # Pydantic schema & /generate endpoint
├── frontend/
│   └── app.py                  # Streamlit UI & Document Exporters
├── Image/
│   ├── generate_logo.py        # Pillow logo generation script
│   └── logo.png                # Branding badge asset
├── exports/                    # Headless export output directory
├── test_all_scenarios.py       # Comprehensive end-to-end test suite
├── PROJECT_REPORT.md           # Formal engineering project report
├── VIVA_VOCE_PREPARATION.md     # 5-member viva defense guide & top 15 Q&As
├── export_report.py            # Converts project report to DOCX & PDF
├── presentation.html           # In-browser Reveal.js/HTML5 slide deck
├── .env                        # Environment credentials (API Key)
├── requirements.txt            # Pinned dependencies
├── run.sh                      # Unix execution launcher
└── run.bat                     # Windows execution launcher
```

---

## ⚖️ Disclaimer
LegalEase is an AI-powered drafting tool intended for informational and operational productivity. It does not constitute formal legal advice. Users should have contracts reviewed by a qualified attorney prior to legal execution.
