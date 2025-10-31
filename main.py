from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_path
import pytesseract
import re
import os

# SETUP PATHS
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
poppler_path = "/usr/bin"  # Poppler utils (installed via apt)

app = FastAPI(title="PDF MCQ Extractor", version="1.0")

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
    extracted_text = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, lang="eng")
        extracted_text += f"\n\n--- Page {i+1} ---\n\n{text}"
    return extracted_text

def extract_mcqs_from_text(text):
    text = text.replace("\r", "")
    text = re.sub(r"Created for Testing Purpose Only", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    mcq_pattern = re.compile(
        r"(\d+\.\s*(?:\[[^\]]+\]\s*)?[^\n]+?\?\s*(?:\n\s*[A-D]\)\s*[^\n]+){2,5})",
        re.MULTILINE,
    )
    return mcq_pattern.findall(text)

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    """Upload a PDF file and extract MCQs."""
    temp_pdf = "temp.pdf"
    with open(temp_pdf, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(temp_pdf)
    mcqs = extract_mcqs_from_text(text)

    os.remove(temp_pdf)
    return {"total_mcqs": len(mcqs), "mcqs": mcqs}
