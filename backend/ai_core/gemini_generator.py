import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from google.genai import types

load_dotenv()


SYSTEM_INSTRUCTIONS = """
You are LegalEase, an AI assistant for drafting legal-document templates.

Create a clear, structured legal draft from the user's supplied information.
Do not invent names, dates, prices, addresses, obligations, or facts that were not supplied.
If information is missing, use a neutral placeholder such as [INSERT ...].
Use plain but professional legal language.
Use headings and numbered sections where useful.
Do not claim that the draft is guaranteed legally valid.
Start with the document title.
Include the supplied parties, terms, and effective date.
Return only the document draft, without Markdown code fences and without commentary.
"""


class GeminiDocumentGenerator:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
        self.fallback_model = os.getenv(
            "GEMINI_FALLBACK_MODEL",
            "gemini-3.6-flash",
        ).strip()

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to the project's .env file."
            )

        self.client = genai.Client(api_key=self.api_key)

    def build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        return f"""
Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date:
{effective_date}

Draft the complete document using only the supplied facts.
""".strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
        )

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            temperature=0.2,
            max_output_tokens=8192,
        )
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
        except APIError as exc:
            if (
                exc.code != 503
                or not self.fallback_model
                or self.fallback_model == self.model
            ):
                raise
            response = self.client.models.generate_content(
                model=self.fallback_model,
                contents=prompt,
                config=config,
            )

        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
