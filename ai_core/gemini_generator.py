import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    """
    Core AI document generation engine utilizing Google Gemini 1.5 Pro
    to produce legally structured, comprehensive, and tailored legal agreements.
    """

    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is not configured. Please provide a valid Gemini API key in your .env file or environment."
            )
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            },
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        """
        Drafts a legally binding, comprehensive legal document based on provided inputs.

        Args:
            document_type: Type of document (e.g. Non-Disclosure Agreement, Employment Contract)
            parties: Descriptions/names of the participating parties and their legal standing
            terms: Key terms, stipulations, and conditions (can be semicolon-separated or bulleted)
            dates: Effective date, termination date, or relevant timeline

        Returns:
            str: Raw markdown-formatted legal document ready for rendering and export.
        """
        prompt = f"""
You are a senior corporate attorney and master legal draftsman. Your task is to draft a formal, legally binding, comprehensive, and enforceable {document_type}.

### INSTRUCTIONS:
1. Use standard, professional legal phrasing and formal legal terminology.
2. Structure the contract with standard legal sections:
   - **TITLE**: Centered and clear document title in uppercase.
   - **PREAMBLE & RECITALS**: Formal identification of the parties, their respective roles, effective date, and recitals stating the background intent ("WHEREAS...").
   - **DEFINED TERMS**: Clear definitions for capitalized key terms used in the contract.
   - **OPERATIVE COVENANTS & OBLIGATIONS**: Detailed clauses based on the supplied terms. Expand and formalize each term into standard, highly protective legal clauses.
   - **CONSIDERATION & PAYMENT / PERFORMANCE**: Terms of compensation, performance, or exchange of value if applicable.
   - **CONFIDENTIALITY & INTELLECTUAL PROPERTY**: Robust confidentiality provisions and IP assignment/protection where applicable.
   - **TERM & TERMINATION**: Duration, termination for convenience, termination for cause, notice periods, and post-termination survival clauses.
   - **REPRESENTATIONS & WARRANTIES**: Standard mutual representations.
   - **INDEMNIFICATION & LIMITATION OF LIABILITY**: Standard liability caps and indemnification scope.
   - **DISPUTE RESOLUTION & GOVERNING LAW**: Choice of law, jurisdiction, and mediation/arbitration provisions.
   - **MISCELLANEOUS / BOILERPLATE**: Severability, Entire Agreement, Amendments, Waivers, Force Majeure, and Notices.
   - **SIGNATURE BLOCKS**: Formal execution blocks for each party with lines for Signature, Printed Name, Title, and Date.

### INPUT DETAILS:
- **Document Type**: {document_type}
- **Parties Involved**: {parties}
- **Terms & Conditions**: {terms}
- **Effective Date & Timelines**: {dates}

### FORMATTING:
- Deliver ONLY the drafted legal document formatted in clean, professional Markdown.
- Use clear numbered section headings (e.g., `1. DEFINITIONS`, `2. OBLIGATIONS OF THE PARTIES`).
- Do not include conversational conversational chatter or meta-commentary before or after the document text.
"""
        try:
            response = self.model.generate_content(prompt)
            if not response or not response.text:
                raise RuntimeError("Empty response received from the Gemini model.")
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini document generation failed: {str(e)}") from e
