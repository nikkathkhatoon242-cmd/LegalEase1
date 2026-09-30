import html
import os
import sys
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from frontend.export_utils import (
    format_docx,
    format_pdf,
    format_txt,
    suggested_filename,
)

load_dotenv()

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "120"))

st.markdown(
    """
    <style>
    .main-title { text-align:center; font-size:2.4rem; font-weight:700; }
    .subtitle { text-align:center; color:#777; margin-bottom:1.5rem; }
    .preview {
        background:#111827; color:#f9fafb; padding:1.5rem;
        border-radius:12px; max-height:600px; overflow-y:auto;
        white-space:pre-wrap; line-height:1.6;
        border:1px solid #374151;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Settings")
    st.caption(f"Backend: {BACKEND_URL}")
    logo = st.file_uploader(
        "Optional logo",
        type=["png", "jpg", "jpeg"],
        help="Used in DOCX and PDF exports for this session.",
    )
    if st.button("Check backend"):
        try:
            response = requests.get(
                f"{BACKEND_URL}/health",
                timeout=10,
            )
            response.raise_for_status()
            st.success("Backend is reachable.")
        except requests.RequestException as exc:
            st.error(f"Backend is not reachable: {exc}")

left, right = st.columns([1, 1])

with left:
    st.subheader("Document details")
    document_type = st.text_input(
        "Document Type",
        placeholder="e.g. Freelance Work Contract",
    )
    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=110,
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=180,
        help="Separate individual terms with semicolons.",
    )
    effective_date = st.text_input(
        "Effective Date",
        placeholder="e.g. April 15, 2026",
    )

    generate = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )

if generate:
    missing = []
    if not document_type.strip():
        missing.append("Document Type")
    if not parties.strip():
        missing.append("Parties Involved")
    if not terms.strip():
        missing.append("Terms & Conditions")
    if not effective_date.strip():
        missing.append("Effective Date")

    if missing:
        st.error("Please complete: " + ", ".join(missing))
    else:
        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.strip(),
        }
        try:
            with st.spinner("Generating your draft..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=TIMEOUT,
                )
            if response.ok:
                data = response.json()
                st.session_state["document_text"] = data["content"]
                st.session_state["document_type"] = data["document_type"]
                st.success("Document generated.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except ValueError:
                    detail = response.text
                st.error(f"Backend error ({response.status_code}): {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to FastAPI. Start the backend first. "
                f"Details: {exc}"
            )

with right:
    st.subheader("Editable preview")
    current_text = st.session_state.get("document_text", "")

    if current_text:
        edited_text = st.text_area(
            "Edit the generated document",
            value=current_text,
            height=430,
            key="editable_document",
        )
        st.session_state["document_text"] = edited_text

        safe_preview = html.escape(edited_text)
        st.markdown(
            f'<div class="preview">{safe_preview}</div>',
            unsafe_allow_html=True,
        )

        doc_type = st.session_state.get(
            "document_type",
            document_type or "LegalEase_Document",
        )
        logo_bytes = logo.getvalue() if logo else None
        base = suggested_filename(doc_type)

        st.markdown("### Download")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "Download TXT",
                data=format_txt(edited_text),
                file_name=f"{base}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                "Download DOCX",
                data=format_docx(edited_text, doc_type, logo_bytes),
                file_name=f"{base}.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )
        with c3:
            st.download_button(
                "Download PDF",
                data=format_pdf(edited_text, doc_type, logo_bytes),
                file_name=f"{base}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.info("Enter the document details and click Generate Document.")

st.divider()
st.caption(
    "LegalEase produces AI-assisted drafts. Review the result and obtain "
    "qualified legal advice where appropriate."
)
