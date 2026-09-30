from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient
from google.genai.errors import APIError

import backend.ai_core.gemini_generator as gemini_generator
import backend.routes as routes
from backend.main import app


class FakeGenerator:
    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        return (
            f"{document_type}\n\n"
            f"Parties: {parties}\n"
            f"Effective Date: {effective_date}\n"
            f"Terms: {terms}"
        )


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate(monkeypatch):
    monkeypatch.setattr(routes, "_generator", FakeGenerator())

    response = client.post(
        "/generate",
        json={
            "document_type": "NDA",
            "parties": "A and B",
            "terms": "Keep information confidential",
            "effective_date": "2026-04-15",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["document_type"] == "NDA"
    assert "confidential" in body["content"].lower()


def test_generate_validation():
    response = client.post(
        "/generate",
        json={
            "document_type": "",
            "parties": "A and B",
            "terms": "Confidential",
            "effective_date": "2026-04-15",
        },
    )
    assert response.status_code == 422


def test_generate_reports_gemini_overload(monkeypatch):
    class OverloadedGenerator:
        def generate_document(
            self,
            document_type: str,
            parties: str,
            terms: str,
            effective_date: str,
        ) -> str:
            raise APIError(
                code=503,
                response_json={
                    "error": {
                        "message": "This model is currently experiencing high demand.",
                        "status": "UNAVAILABLE",
                    }
                },
            )

    monkeypatch.setattr(routes, "_generator", OverloadedGenerator())

    response = client.post(
        "/generate",
        json={
            "document_type": "NDA",
            "parties": "A and B",
            "terms": "Keep information confidential",
            "effective_date": "2026-04-15",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Gemini is temporarily overloaded. Please try again shortly."
    )
    assert response.headers["retry-after"] == "30"


def test_generator_uses_fallback_model_after_overload(monkeypatch):
    client = Mock()
    client.models.generate_content.side_effect = [
        APIError(
            code=503,
            response_json={"error": {"status": "UNAVAILABLE"}},
        ),
        SimpleNamespace(text="Fallback draft"),
    ]
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.8-flash")
    monkeypatch.setenv("GEMINI_FALLBACK_MODEL", "gemini-3.6-flash")
    monkeypatch.setattr(gemini_generator.genai, "Client", lambda **kwargs: client)

    generator = gemini_generator.GeminiDocumentGenerator()
    result = generator.generate_document(
        document_type="NDA",
        parties="A and B",
        terms="Keep information confidential",
        effective_date="2026-04-15",
    )

    assert result == "Fallback draft"
    assert [
        call.kwargs["model"]
        for call in client.models.generate_content.call_args_list
    ] == ["gemini-3.8-flash", "gemini-3.6-flash"]
