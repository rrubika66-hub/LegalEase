from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import sys
import os

# Add parent directory to sys.path to ensure module imports work smoothly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter(tags=["Document Generation"])

class DocumentRequest(BaseModel):
    """
    Schema for legal document generation requests.
    """
    document_type: str = Field(
        ..., 
        description="The type of legal document to generate",
        example="Non-Disclosure Agreement (NDA)"
    )
    parties: str = Field(
        ..., 
        description="Names, roles, and entities of all involved parties",
        example="Disclosing Party: Acme Corp, 123 Tech Blvd; Receiving Party: John Doe, Consultant"
    )
    terms: str = Field(
        ..., 
        description="Key terms, covenants, and restrictions separated by semicolons or in bullet points",
        example="2-year non-disclosure duration; standard trade secrets protection; jurisdiction in California"
    )
    dates: str = Field(
        ..., 
        description="Effective date, duration, and key milestones",
        example="Effective October 1, 2024 with a 2-year term"
    )

class DocumentResponse(BaseModel):
    """
    Response schema returning generated document text.
    """
    document: str

@router.post("/generate", response_model=DocumentResponse, status_code=status.HTTP_200_OK)
async def generate_legal_document(request: DocumentRequest):
    """
    Endpoint to trigger Gemini 1.5 Pro AI drafting of legal agreements.
    """
    try:
        generator = GeminiDocumentGenerator()
        generated_doc = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )
        return DocumentResponse(document=generated_doc)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate legal document: {str(e)}"
        )
