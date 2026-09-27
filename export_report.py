"""
LegalEase Project Report Exporter
Converts PROJECT_REPORT.md into production-formatted .docx and .pdf files.
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from frontend.app import create_docx, create_pdf

def export_reports():
    report_md_path = os.path.join(CURRENT_DIR, "PROJECT_REPORT.md")
    if not os.path.exists(report_md_path):
        print(f"Error: Could not find {report_md_path}")
        return

    with open(report_md_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    print("=============================================================")
    print("        LegalEase: Project Report Document Exporter          ")
    print("=============================================================")

    # 1. Export DOCX
    docx_output_path = os.path.join(CURRENT_DIR, "PROJECT_REPORT.docx")
    try:
        docx_stream = create_docx(report_text)
        with open(docx_output_path, "wb") as f:
            f.write(docx_stream.getvalue())
        print(f"✅ Generated Word Document: {docx_output_path} ({os.path.getsize(docx_output_path)} bytes)")
    except Exception as e:
        print(f"❌ Failed to generate DOCX: {e}")

    # 2. Export PDF
    pdf_output_path = os.path.join(CURRENT_DIR, "PROJECT_REPORT.pdf")
    try:
        pdf_stream = create_pdf(report_text)
        with open(pdf_output_path, "wb") as f:
            f.write(pdf_stream.getvalue())
        print(f"✅ Generated PDF Document:  {pdf_output_path} ({os.path.getsize(pdf_output_path)} bytes)")
    except Exception as e:
        print(f"❌ Failed to generate PDF: {e}")

    print("=============================================================\n")

if __name__ == "__main__":
    export_reports()
