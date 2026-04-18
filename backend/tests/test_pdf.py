import os
import fitz
from app.services.pdf_service import extract_text_from_pdf

def test_pdf_extraction():
    dir_path = "backend/data/pdfs"
    file_path = os.path.join(dir_path, "sample.pdf")

    # Ensure directory exists
    os.makedirs(dir_path, exist_ok=True)

    # Create dummy PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello World PDF")
    doc.save(file_path)
    doc.close()

    text = extract_text_from_pdf(file_path)

    assert isinstance(text, str)
    assert "Hello World" in text