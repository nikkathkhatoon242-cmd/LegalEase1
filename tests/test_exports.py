from docx import Document
from frontend.export_utils import format_docx, format_pdf, format_txt


SAMPLE = """NON-DISCLOSURE AGREEMENT

1. PARTIES
Alice Smith and ABC Technologies.

2. CONFIDENTIALITY
- Confidential information must not be disclosed.
- Public information is excluded.
"""


def test_txt_export():
    data = format_txt(SAMPLE)
    assert data.startswith(b"NON-DISCLOSURE")


def test_docx_export():
    data = format_docx(SAMPLE, "Non-Disclosure Agreement")
    assert data[:2] == b"PK"
    assert len(data) > 1000


def test_pdf_export():
    data = format_pdf(SAMPLE, "Non-Disclosure Agreement")
    assert data.startswith(b"%PDF")
    assert len(data) > 1000
