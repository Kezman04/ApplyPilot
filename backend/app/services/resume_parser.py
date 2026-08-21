from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_resume_text(filename: str, content: bytes) -> str:
    filename_lower = filename.lower()

    if filename_lower.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    if filename_lower.endswith(".pdf"):
        reader = PdfReader(BytesIO(content))
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts)

    if filename_lower.endswith(".docx"):
        document = Document(BytesIO(content))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    raise ValueError("Unsupported file type")