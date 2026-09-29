import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

class GeminiDocumentGenerator:
    """
    Core document generator powered by Google Gemini 1.5 Pro.
    Generates legally binding, structured legal agreements.
    """

    def __init__(self, api_key: str = None):
        # Retrieve API key from parameter or environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is not set or is using the placeholder. "
                "Please configure your valid API key in the .env file."
            )
        
        # Configure the Google Generative AI SDK
        genai.configure(api_key=self.api_key)
        
        # Generation configuration for high precision legal text
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        # Safety settings for legal document drafting
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        # Initialize Gemini 1.5 Pro model
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Drafts a comprehensive, formal legal document based on user inputs.

        :param document_type: The type of legal document (e.g., NDA, Employment Contract, Lease Agreement).
        :param parties: Description of all involved parties and their legal designations.
        :param terms: Core terms, conditions, obligations, and covenants (semicolon-separated or free text).
        :param dates: Effective date, duration, expiration, or milestones.
        :return: Raw formatted markdown text of the complete legal document.
        """
        system_prompt = f"""You are a senior legal counsel and professional contract drafting attorney. 
Draft a complete, formal, legally binding, and comprehensive legal document based on the following specifications:

Document Type: {document_type}
Parties Involved: {parties}
Key Terms & Conditions: {terms}
Effective Date & Timeline: {dates}

Drafting Requirements:
1. Format with professional legal structure using clear Markdown headings (e.g., # TITLE, ## Section Name):
   - TITLE OF THE AGREEMENT (in all caps, centered style)
   - PREAMBLE & RECITALS (e.g., "This Agreement is entered into on...", "WHEREAS...")
   - DEFINED TERMS / DEFINITIONS
   - OPERATIVE CLAUSES / RIGHTS AND OBLIGATIONS (detailed, standard legal boilerplate tailored to the specific type)
   - CONSIDERATION & PAYMENT (if applicable)
   - CONFIDENTIALITY, REPRESENTATIONS & WARRANTIES
   - TERM, TERMINATION & DEFAULT
   - INDEMNIFICATION & LIMITATION OF LIABILITY
   - DISPUTE RESOLUTION & GOVERNING LAW / JURISDICTION
   - MISCELLANEOUS / GENERAL PROVISIONS (Severability, Entire Agreement, Amendments, Counterparts)
   - SIGNATURE BLOCKS (Formal signature spaces for all named parties, including Name, Title, Company, Date, and Signature lines).

2. Use precise legal terminology (e.g., "shall", "covenants", "indemnify and hold harmless").
3. Ensure no placeholder brackets like "[Insert Date Here]" remain unfilled if the information is provided in the inputs.
4. Provide the complete text in clean, professional markdown format ready for export.
"""

        try:
            response = self.model.generate_content(system_prompt)
            if response and response.text:
                return response.text
            else:
                raise RuntimeError("Empty response received from Gemini model.")
        except Exception as e:
            raise RuntimeError(f"Error generating document with Gemini AI: {str(e)}")
