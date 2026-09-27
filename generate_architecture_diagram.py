"""
LegalEase System Architecture Diagram Generator
Uses Pillow to create a high-resolution, dark-mode system architecture diagram (Image/system_architecture.png).
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_architecture_diagram(output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Supersampling 2x (Canvas 2000 x 1300 downsampled to 1000 x 650)
    width, height = 2000, 1300
    img = Image.new("RGBA", (width, height), color=(15, 23, 42, 255)) # Dark navy background (#0f172a)
    draw = ImageDraw.Draw(img)

    # Color Palette
    bg_card = (30, 41, 59, 240)      # Slate 800 (#1e293b)
    bg_card_ai = (49, 46, 129, 240)   # Indigo 900 (#312e81)
    border_cyan = (56, 189, 248, 255) # Sky 400 (#38bdf8)
    border_purple = (192, 132, 252, 255) # Purple 400 (#c084fc)
    border_emerald = (52, 211, 153, 255) # Emerald 400 (#34d399)
    text_white = (248, 250, 252, 255) # Slate 50
    text_dim = (148, 163, 184, 255)   # Slate 400
    arrow_color = (96, 165, 250, 255) # Blue 400

    # Fonts
    try:
        font_header = ImageFont.truetype("arial.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 26)
        font_card_title = ImageFont.truetype("arialbd.ttf", 34)
        font_card_sub = ImageFont.truetype("arial.ttf", 22)
        font_badge = ImageFont.truetype("arialbd.ttf", 20)
    except Exception:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_card_title = ImageFont.load_default()
        font_card_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Draw Header & Title
    draw.text((100, 60), "LEGALESE AI : SYSTEM ARCHITECTURE", fill=text_white, font=font_header)
    draw.text((100, 120), "End-to-End Production Microservice & Generative AI Pipeline", fill=text_dim, font=font_sub)
    draw.line([(100, 165), (1900, 165)], fill=(51, 65, 85, 255), width=3)

    # 1. Box: CLIENT LAYER (Streamlit)
    draw.rounded_rectangle([(100, 210), (920, 580)], radius=20, fill=bg_card, outline=border_cyan, width=4)
    draw.rounded_rectangle([(120, 230), (320, 275)], radius=10, fill=(14, 116, 144, 255))
    draw.text((135, 240), "CLIENT LAYER", fill=text_white, font=font_badge)
    draw.text((120, 290), "Streamlit Web Interface (Port 8501)", fill=border_cyan, font=font_card_title)
    lines_client = [
        "• Parameterized Input Form (Parties, Terms, Dates)",
        "• Dynamic In-Browser Inline Editor (st.text_area)",
        "• State Persistence (st.session_state)",
        "• Live Formatted Markdown Preview Container"
    ]
    for i, line in enumerate(lines_client):
        draw.text((120, 350 + (i * 45)), line, fill=text_white, font=font_card_sub)

    # 2. Box: API LAYER (FastAPI)
    draw.rounded_rectangle([(1080, 210), (1900, 580)], radius=20, fill=bg_card, outline=border_cyan, width=4)
    draw.rounded_rectangle([(1100, 230), (1330, 275)], radius=10, fill=(3, 105, 161, 255))
    draw.text((1115, 240), "BACKEND API LAYER", fill=text_white, font=font_badge)
    draw.text((1100, 290), "FastAPI Microservice (Port 8000)", fill=border_cyan, font=font_card_title)
    lines_api = [
        "• Pydantic Model Validation (DocumentRequest)",
        "• Cross-Origin Resource Sharing (CORS) Middleware",
        "• Granular Exception Boundaries (422 / 400 / 500)",
        "• OpenAPI Interactive Docs (/docs & /redoc)"
    ]
    for i, line in enumerate(lines_api):
        draw.text((1100, 350 + (i * 45)), line, fill=text_white, font=font_card_sub)

    # Arrow 1: Client -> Backend (HTTP POST)
    draw.line([(920, 395), (1080, 395)], fill=arrow_color, width=6)
    draw.polygon([(1080, 395), (1050, 380), (1050, 410)], fill=arrow_color)
    draw.text((935, 350), "HTTP POST /generate", fill=border_cyan, font=font_card_sub)

    # 3. Box: AI CORE (Gemini 1.5 Pro)
    draw.rounded_rectangle([(1080, 680), (1900, 1150)], radius=20, fill=bg_card_ai, outline=border_purple, width=4)
    draw.rounded_rectangle([(1100, 700), (1330, 745)], radius=10, fill=(109, 40, 217, 255))
    draw.text((1115, 710), "AI GENERATION CORE", fill=text_white, font=font_badge)
    draw.text((1100, 760), "Google Gemini 1.5 Pro", fill=border_purple, font=font_card_title)
    lines_ai = [
        "• Zero-Shot Senior Attorney Prompt Framework",
        "• Low-Temperature Calibration (temperature = 0.2)",
        "• 8-Tier Legal Structure (Recitals -> Clauses -> Signatures)",
        "• 8192 Max Output Token Window (Full Agreement)"
    ]
    for i, line in enumerate(lines_ai):
        draw.text((1100, 820 + (i * 45)), line, fill=text_white, font=font_card_sub)

    # Arrow 2: Backend -> AI Core
    draw.line([(1490, 580), (1490, 680)], fill=border_purple, width=6)
    draw.polygon([(1490, 680), (1475, 650), (1505, 650)], fill=border_purple)
    draw.text((1510, 615), "SDK Method Call", fill=border_purple, font=font_card_sub)

    # 4. Box: EXPORT PIPELINE (.TXT, .DOCX, .PDF)
    draw.rounded_rectangle([(100, 680), (920, 1150)], radius=20, fill=bg_card, outline=border_emerald, width=4)
    draw.rounded_rectangle([(120, 700), (360, 745)], radius=10, fill=(4, 120, 87, 255))
    draw.text((135, 710), "EXPORT PIPELINE", fill=text_white, font=font_badge)
    draw.text((120, 760), "Multi-Format Headless Exporters", fill=border_emerald, font=font_card_title)
    lines_export = [
        "• Plain Text (.txt) UTF-8 Export",
        "• Word (.docx) via python-docx (1\" margins, Times New Roman)",
        "• PDF (.pdf) via fpdf2 with Latin-1 Unicode Sanitization",
        "• Automated Headless Test Suite (test_all_scenarios.py)"
    ]
    for i, line in enumerate(lines_export):
        draw.text((120, 820 + (i * 45)), line, fill=text_white, font=font_card_sub)

    # Arrow 3: AI Core -> Client -> Exporters
    draw.line([(1080, 915), (920, 915)], fill=border_emerald, width=6)
    draw.polygon([(920, 915), (950, 900), (950, 930)], fill=border_emerald)
    draw.text((945, 870), "Raw Markdown", fill=border_emerald, font=font_card_sub)

    # Downsample for crisp edges
    final_img = img.resize((1000, 650), Image.Resampling.LANCZOS)
    final_img.save(output_path, "PNG")
    print(f"✅ Generated high-resolution architecture diagram at: {output_path}")

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Image", "system_architecture.png")
    generate_architecture_diagram(target)
