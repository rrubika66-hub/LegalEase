from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter(tags=["Document Generation"])

class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        description="The type of legal document to generate (e.g. Non-Disclosure Agreement, Employment Contract)",
        example="Non-Disclosure Agreement (NDA)",
    )
    parties: str = Field(
        ...,
        description="The names and descriptions of participating parties",
        example="Disclosing Party: Acme Corp (Delaware Corp); Receiving Party: John Doe (Independent Consultant)",
    )
    terms: str = Field(
        ...,
        description="Key terms, stipulations, and clauses (semicolon-separated or freeform)",
        example="2-year non-disclosure period; Return of confidential materials within 10 days of termination; Mutual non-solicitation for 12 months; Governing law State of California",
    )
    dates: str = Field(
        ...,
        description="Effective date and other timeline specifications",
        example="Effective as of October 1, 2026",
    )

class DocumentResponse(BaseModel):
    document: str = Field(..., description="The complete generated legal agreement text in Markdown format")

@router.post(
    "/generate",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Legal Document",
    description="Processes document specifications and calls Gemini 1.5 Pro to produce a comprehensive legal contract.",
)
async def generate_document_endpoint(request: DocumentRequest):
    if not request.document_type.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="document_type cannot be empty.",
        )
    if not request.parties.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="parties cannot be empty.",
        )
    if not request.terms.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="terms cannot be empty.",
        )

    try:
        generator = GeminiDocumentGenerator()
        generated_doc = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return DocumentResponse(document=generated_doc)
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err),
        ) from val_err
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate legal document: {str(exc)}",
        ) from exc
