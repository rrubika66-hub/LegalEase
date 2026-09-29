import io
import os
import re
import requests
import streamlit as st
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

# Page Configuration
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism & Professional Legal Aesthetics)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    .main-header h1 {
        font-family: 'Merriweather', serif;
        font-size: 2.2rem;
        color: #f8fafc;
        margin: 0;
    }
    
    .main-header p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3);
    }
    
    .preview-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        font-family: 'Merriweather', serif;
        line-height: 1.8;
        color: #1e293b;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .sidebar-info {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        font-size: 0.85rem;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# Helper: Ensure Logo Exists or Generate Placeholder
def get_or_create_logo():
    img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Image")
    os.makedirs(img_dir, exist_ok=True)
    logo_path = os.path.join(img_dir, "logo.png")
    
    if not os.path.exists(logo_path):
        # Create a clean brand badge using PIL
        img = Image.new("RGBA", (300, 80), color=(15, 23, 42, 255))
        draw = ImageDraw.Draw(img)
        # Draw scales symbol & text
        draw.rectangle([10, 10, 70, 70], fill=(37, 99, 235, 255))
        draw.text((25, 20), "§", fill=(255, 255, 255, 255))
        draw.text((85, 25), "LegalEase", fill=(248, 250, 252, 255))
        img.save(logo_path, "PNG")
    
    return logo_path

# Helper: Export to DOCX
def create_docx(text: str, document_title: str) -> io.BytesIO:
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    
    # Add Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(document_title.upper())
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    doc.add_paragraph() # Spacer
    
    # Process text lines
    lines = text.split("\n")
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        
        # Check for headings
        if line_clean.startswith("###"):
            h = doc.add_paragraph()
            r = h.add_run(line_clean.replace("###", "").strip())
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.font.bold = True
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(4)
        elif line_clean.startswith("##"):
            h = doc.add_paragraph()
            r = h.add_run(line_clean.replace("##", "").strip())
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            r.font.bold = True
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(4)
        elif line_clean.startswith("#"):
            h = doc.add_paragraph()
            r = h.add_run(line_clean.replace("#", "").strip())
            r.font.name = "Times New Roman"
            r.font.size = Pt(14)
            r.font.bold = True
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(6)
        else:
            p = doc.add_paragraph()
            # Remove Markdown bold formatting syntax for clean Word document
            cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', line_clean)
            r = p.add_run(cleaned_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(6)
            
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Helper: Sanitize string for standard PDF encoders
def sanitize_for_pdf(text: str) -> str:
    replacements = {
        '—': '-', '–': '-', '“': '"', '”': '"', '‘': "'", '’': "'",
        '…': '...', '•': '*', '§': 'Section ', '©': '(C)', '®': '(R)',
        '™': '(TM)', '\u200b': '', '\u2013': '-', '\u2014': '-'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    # Ensure all characters fit standard latin-1 / ascii fallback
    return text.encode('latin-1', 'replace').decode('latin-1')

# Custom PDF Class with Header and Footer
class LegalPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, sanitize_for_pdf('CONFIDENTIAL - LEGAL DOCUMENT'), 0, 0, 'R')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Helper: Export to PDF
def create_pdf(text: str, document_title: str) -> io.BytesIO:
    pdf = LegalPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    
    # Document Title
    pdf.set_font("Helvetica", 'B', 15)
    pdf.set_text_color(15, 23, 42)
    sanitized_title = sanitize_for_pdf(document_title.upper())
    pdf.cell(0, 10, sanitized_title, ln=True, align='C')
    pdf.ln(5)
    
    lines = text.split("\n")
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            pdf.ln(3)
            continue
            
        if line_clean.startswith("###"):
            pdf.set_font("Helvetica", 'B', 11)
            pdf.set_text_color(30, 41, 59)
            heading_txt = sanitize_for_pdf(line_clean.replace("###", "").strip())
            pdf.ln(2)
            pdf.multi_cell(0, 6, heading_txt)
            pdf.ln(1)
        elif line_clean.startswith("##") or line_clean.startswith("#"):
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_text_color(15, 23, 42)
            heading_txt = sanitize_for_pdf(line_clean.lstrip("#").strip())
            pdf.ln(4)
            pdf.multi_cell(0, 7, heading_txt)
            pdf.ln(2)
        else:
            pdf.set_font("Helvetica", '', 10)
            pdf.set_text_color(30, 41, 59)
            cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', line_clean)
            sanitized_body = sanitize_for_pdf(cleaned_text)
            pdf.multi_cell(0, 5.5, sanitized_body)
            pdf.ln(1.5)
            
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


# Main Application Interface
def main():
    # Sidebar
    with st.sidebar:
        logo_path = get_or_create_logo()
        if os.path.exists(logo_path):
            st.image(logo_path, use_column_width=True)
            
        st.markdown("### ⚖️ About LegalEase")
        st.markdown(
            "LegalEase is an AI-powered legal document generation platform "
            "designed to draft contract agreements, NDAs, service pacts, and "
            "custom legal instruments instantly."
        )
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-info">
            <strong>Supported Document Types:</strong><br/>
            • Non-Disclosure Agreement (NDA)<br/>
            • Employment Agreement<br/>
            • Independent Contractor Contract<br/>
            • Commercial Lease Agreement<br/>
            • Software Service Agreement (SaaS)<br/>
            • Partnership Agreement
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        api_url = st.text_input("Backend API Endpoint", value="http://localhost:8000")

    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ LegalEase AI</h1>
        <p>Intelligent Legal Contract & Document Drafting Engine</p>
    </div>
    """, unsafe_allow_html=True)

    # Document Inputs Form
    with st.container():
        st.subheader("📋 Document Specifications")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            document_type = st.text_input(
                "Document Type *",
                placeholder="e.g. Non-Disclosure Agreement (NDA)",
                help="Type or select the legal agreement category."
            )
        with col2:
            dates = st.text_input(
                "Effective Date & Timeline *",
                placeholder="e.g. Effective October 1, 2024 for a duration of 2 years",
                help="Specify key dates, term lengths, or milestone timelines."
            )
            
        parties = st.text_area(
            "Parties Involved *",
            placeholder="e.g. Party A (Disclosing Party): Apex Innovations Inc., 100 Silicon Ave;\nParty B (Receiving Party): Jane Doe, Consultant, 456 Oak Lane",
            help="List all participating individuals or legal entities with designations and addresses."
        )
        
        terms = st.text_area(
            "Terms & Conditions (semicolon-separated) *",
            placeholder="e.g. Confidentiality duration 24 months; Governing law of Delaware; Non-solicitation of employees; Liquidated damages of $50,000 for breach",
            help="Detail the key terms, covenants, payments, restrictions, and governing clauses."
        )
        
        generate_btn = st.button("⚡ Generate Document", use_container_width=True)

    # Session State Initialization for Persistence
    if "generated_doc" not in st.session_state:
        st.session_state.generated_doc = ""
    if "current_doc_type" not in st.session_state:
        st.session_state.current_doc_type = "Legal_Document"

    # Handle Generation
    if generate_btn:
        if not document_type or not parties or not terms or not dates:
            st.error("⚠️ Please fill in all required fields to draft the legal document.")
        else:
            with st.spinner("⚖️ Consulting Gemini 1.5 Pro legal intelligence..."):
                payload = {
                    "document_type": document_type,
                    "parties": parties,
                    "terms": terms,
                    "dates": dates
                }
                try:
                    res = requests.post(f"{api_url.rstrip('/')}/generate", json=payload, timeout=90)
                    if res.status_code == 200:
                        doc_text = res.json().get("document", "")
                        st.session_state.generated_doc = doc_text
                        st.session_state.current_doc_type = document_type
                        st.success("✅ Legal document successfully generated!")
                    else:
                        detail = res.json().get("detail", res.text)
                        st.error(f"❌ API Error ({res.status_code}): {detail}")
                except requests.exceptions.ConnectionError:
                    st.error(f"❌ Could not reach the backend server at `{api_url}`. Please ensure FastAPI is running via `run.sh` or `uvicorn`.")
                except Exception as ex:
                    st.error(f"❌ An error occurred: {str(ex)}")

    # Display & Export Section
    if st.session_state.generated_doc:
        st.markdown("---")
        st.subheader("📄 Generated Document Preview & Inline Editor")
        
        # Inline Editable Text Area
        edited_doc = st.text_area(
            "Modify or refine the text before exporting:",
            value=st.session_state.generated_doc,
            height=350
        )
        
        # Format filename
        file_prefix = re.sub(r'[^a-zA-Z0-9]', '_', st.session_state.current_doc_type).strip('_') or "Legal_Agreement"
        
        st.markdown("### 📥 Export Options")
        col_txt, col_docx, col_pdf = st.columns(3)
        
        # 1. TXT Download
        with col_txt:
            st.download_button(
                label="📄 Download .TXT",
                data=edited_doc.encode('utf-8'),
                file_name=f"{file_prefix}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        # 2. DOCX Download
        with col_docx:
            try:
                docx_buffer = create_docx(edited_doc, st.session_state.current_doc_type)
                st.download_button(
                    label="📝 Download .DOCX",
                    data=docx_buffer,
                    file_name=f"{file_prefix}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            except Exception as e:
                st.warning(f"DOCX preparation error: {e}")
                
        # 3. PDF Download
        with col_pdf:
            try:
                pdf_buffer = create_pdf(edited_doc, st.session_state.current_doc_type)
                st.download_button(
                    label="📑 Download .PDF",
                    data=pdf_buffer,
                    file_name=f"{file_prefix}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.warning(f"PDF preparation error: {e}")

if __name__ == "__main__":
    main()
