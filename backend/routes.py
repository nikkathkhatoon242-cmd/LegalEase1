from fastapi import APIRouter, HTTPException
from google.genai.errors import APIError

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest, DocumentResponse

router = APIRouter()
_generator: GeminiDocumentGenerator | None = None


def get_generator() -> GeminiDocumentGenerator:
    global _generator
    if _generator is None:
        _generator = GeminiDocumentGenerator()
    return _generator


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    try:
        content = get_generator().generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
        )
    except APIError as exc:
        if exc.code == 503:
            raise HTTPException(
                status_code=503,
                detail=(
                    "Gemini is temporarily overloaded. Please try again shortly."
                ),
                headers={"Retry-After": "30"},
            ) from exc
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc
