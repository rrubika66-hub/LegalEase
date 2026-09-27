import os
import io
import requests
import streamlit as st
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="LegalEase",
    layout="centered",
    page_icon="⚖️",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished, modern legal aesthetic
st.markdown(
    """
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 860px;
    }
    
    /* Header card */
    .legal-header {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        margin-bottom: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .legal-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #f8fafc;
    }
    .legal-header p {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 0;
    }

    /* Document preview container */
    .doc-preview-container {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 2.5rem 3rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        font-family: 'Times New Roman', Times, serif;
        color: #0f172a;
        line-height: 1.7;
        margin: 1.5rem 0;
    }

    /* Primary button style */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Document Exporter Utilities
# ---------------------------------------------------------
def create_docx(markdown_text: str) -> io.BytesIO:
    """Generates a professionally formatted Microsoft Word (.docx) document."""
    doc = Document()

    # Standard 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base styling
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    for raw_line in markdown_text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            p = doc.add_heading(line.lstrip("# ").strip(), level=1)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(16)
                run.font.bold = True
                run.font.color.rgb = RGBColor(15, 23, 42)
        elif line.startswith("## "):
            p = doc.add_heading(line.lstrip("# ").strip(), level=2)
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)
                run.font.bold = True
                run.font.color.rgb = RGBColor(30, 41, 59)
        elif line.startswith("### "):
            p = doc.add_heading(line.lstrip("# ").strip(), level=3)
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(11.5)
                run.font.bold = True
                run.font.color.rgb = RGBColor(51, 65, 85)
        elif line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(line[2:], style="List Bullet")
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(4)
        elif (
            len(line) > 2
            and line[0].isdigit()
            and line[1] in [".", ")"]
        ):
            p = doc.add_paragraph(line[2:].strip(), style="List Number")
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(4)
        else:
            p = doc.add_paragraph(line)
            p.paragraph_format.line_spacing = 1.2
            p.paragraph_format.space_after = Pt(6)

    docx_buffer = io.BytesIO()
    doc.save(docx_buffer)
    docx_buffer.seek(0)
    return docx_buffer


def sanitize_text_for_pdf(text: str) -> str:
    """Sanitizes unicode characters to avoid latin-1 encoding errors in standard FPDF."""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2014": " - ",
        "\u2013": " - ",
        "\u2022": "*",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2122": "(TM)",
        "\u00ae": "(R)",
        "\u00a9": "(C)",
        "§": "Section ",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text.encode("latin-1", "replace").decode("latin-1")


class LegalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, "CONFIDENTIAL LEGAL DOCUMENT", border=0, align="R")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        page_str = f"Page {self.page_no()}"
        self.cell(0, 10, page_str, border=0, align="C")


def create_pdf(markdown_text: str) -> io.BytesIO:
    """Generates a clean, paginated PDF with margins, header, footer, and sanitized text."""
    pdf = LegalPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(left=20, top=20, right=20)
    pdf.add_page()

    sanitized = sanitize_text_for_pdf(markdown_text)
    for raw_line in sanitized.split("\n"):
        line = raw_line.strip()
        if not line:
            pdf.ln(3)
            continue

        if line.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(0, 7, line.lstrip("# ").strip(), align="C")
            pdf.ln(3)
        elif line.startswith("## "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 6, line.lstrip("# ").strip(), align="L")
            pdf.ln(2)
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 5, line.lstrip("# ").strip(), align="L")
            pdf.ln(1)
        elif line.startswith(("- ", "* ")):
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5, f"  * {line[2:]}", align="L")
            pdf.ln(1)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(0, 5, line, align="L")
            pdf.ln(2)

    pdf_buffer = io.BytesIO()
    pdf_bytes = pdf.output()
    if isinstance(pdf_bytes, str):
        pdf_buffer.write(pdf_bytes.encode("latin-1"))
    elif isinstance(pdf_bytes, (bytes, bytearray)):
        pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)
    return pdf_buffer


# ---------------------------------------------------------
# UI Header & Logo
# ---------------------------------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "..", "Image", "logo.png")
if os.path.exists(logo_path):
    try:
        logo_img = Image.open(logo_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_img, use_container_width=True)
    except Exception:
        pass

st.markdown(
    """
    <div class="legal-header">
        <h1>⚖️ LegalEase</h1>
        <p>AI-Powered Production-Grade Legal Document Generator</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    default_backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000/generate")
    api_url = st.text_input("Backend API URL", value=default_backend_url)
    st.markdown("---")
    st.markdown("### 💡 Tips for Best Results")
    st.markdown(
        """
        - **Parties**: Include full legal names, jurisdiction of formation, or residential addresses.
        - **Terms**: Separate distinct covenants with semicolons.
        - **Dates**: Clearly specify effective dates and milestone periods.
        """
    )

# ---------------------------------------------------------
# Document Generation Form
# ---------------------------------------------------------
st.subheader("📝 Document Specifications")

with st.form(key="document_generation_form"):
    doc_type = st.text_input(
        "Document Type *",
        placeholder="e.g. Non-Disclosure Agreement (NDA), Employment Agreement, Commercial Lease",
        help="Specify the legal contract type you want drafted.",
    )

    parties = st.text_area(
        "Parties Involved *",
        placeholder="Party A (Discloser): NexaTech Solutions Inc., a Delaware corporation\nParty B (Recipient): Johnathan Davis, an individual residing in New York",
        height=100,
        help="List all participating parties with their legal statuses.",
    )

    terms = st.text_area(
        "Terms & Conditions (semicolon-separated) *",
        placeholder="Term of confidentiality shall be 3 years; Return of all confidential materials within 14 days of termination; Mutual non-solicitation of employees for 12 months; Governing law State of New York; Dispute resolution via binding AAA arbitration in NYC.",
        height=140,
        help="Enter the operative clauses, covenants, and conditions.",
    )

    dates = st.text_input(
        "Effective Date & Key Dates *",
        placeholder="Effective as of October 1, 2026; Termination date December 31, 2027",
        help="Provide effective dates, termination dates, or milestone timelines.",
    )

    submit_button = st.form_submit_button(label="🚀 Generate Document", type="primary")

# Initialize session state for document persistence
if "generated_doc" not in st.session_state:
    st.session_state.generated_doc = ""
if "doc_type_saved" not in st.session_state:
    st.session_state.doc_type_saved = "Legal_Document"

if submit_button:
    if not doc_type.strip() or not parties.strip() or not terms.strip() or not dates.strip():
        st.error("⚠️ Please fill in all required fields marked with * before submitting.")
    else:
        payload = {
            "document_type": doc_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "dates": dates.strip(),
        }

        with st.spinner("⚖️ Consulting Gemini 1.5 Pro legal drafting engine... Please wait."):
            try:
                response = requests.post(api_url, json=payload, timeout=90)
                if response.status_code == 200:
                    result_data = response.json()
                    st.session_state.generated_doc = result_data.get("document", "")
                    st.session_state.doc_type_saved = doc_type.strip().replace(" ", "_")
                    st.success("✅ Legal document successfully generated!")
                else:
                    detail = response.json().get("detail", response.text)
                    st.error(f"❌ Generation failed ({response.status_code}): {detail}")
            except requests.exceptions.ConnectionError:
                st.error(
                    f"❌ Unable to connect to backend at `{api_url}`. "
                    "Make sure the FastAPI server is running (`uvicorn legalEaseAPI.main:app --port 8000`)."
                )
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")

# ---------------------------------------------------------
# Dynamic Preview, Inline Editing & Exporters
# ---------------------------------------------------------
if st.session_state.generated_doc:
    st.markdown("---")
    st.subheader("📄 Generated Document Preview & Inline Editor")
    st.caption("You can modify the document directly below before exporting to your preferred format.")

    # Inline Editor
    edited_doc = st.text_area(
        label="Edit Document Content",
        value=st.session_state.generated_doc,
        height=450,
        key="doc_editor",
    )
    st.session_state.generated_doc = edited_doc

    # Styled Formatted Preview Expandable
    with st.expander("👁️ View Formatted Markdown Preview", expanded=False):
        st.markdown(
            f'<div class="doc-preview-container">{st.session_state.generated_doc}</div>',
            unsafe_allow_html=True,
        )

    # Exporters / Download Buttons
    st.markdown("### 💾 Export & Download")
    col1, col2, col3 = st.columns(3)
    file_base_name = f"{st.session_state.doc_type_saved}_Draft"

    with col1:
        # 1. Plain Text (.txt) Download
        st.download_button(
            label="📄 Download .TXT",
            data=st.session_state.generated_doc.encode("utf-8"),
            file_name=f"{file_base_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        # 2. Microsoft Word (.docx) Download
        try:
            docx_data = create_docx(st.session_state.generated_doc)
            st.download_button(
                label="📘 Download .DOCX",
                data=docx_data,
                file_name=f"{file_base_name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        except Exception as docx_err:
            st.error(f"Error preparing DOCX: {docx_err}")

    with col3:
        # 3. PDF (.pdf) Download
        try:
            pdf_data = create_pdf(st.session_state.generated_doc)
            st.download_button(
                label="📕 Download .PDF",
                data=pdf_data,
                file_name=f"{file_base_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as pdf_err:
            st.error(f"Error preparing PDF: {pdf_err}")
