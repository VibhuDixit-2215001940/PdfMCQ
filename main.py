import pytesseract
from pdf2image import convert_from_path
import os
import re
 
 
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\VibhuDixit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
 
 
poppler_path = r"C:\poppler-25.07.0\Library\bin"

 
 
def extract_text_from_pdf(pdf_path, output_txt_path="output.txt"):
    """Extracts text from all pages in a PDF using OCR"""
    print("[INFO] Converting PDF to images...")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
 
    extracted_text = ""
    for i, page in enumerate(pages):
        print(f"[INFO] Processing page {i + 1}/{len(pages)}...")
        text = pytesseract.image_to_string(page, lang="eng")
        extracted_text += f"\n\n--- Page {i + 1} ---\n\n{text}"
 
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
 
    print(f"[✅] Text extraction complete! Saved to {output_txt_path}")
    return extracted_text
 
 
def extract_mcqs_from_text(text):
    """Extracts MCQs from OCR text (handles multi-line and noisy OCR data)"""
 
   
    text = text.replace("\r", "")
    text = re.sub(r"Created for Testing Purpose Only", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
 
   
    mcq_pattern = re.compile(
        r"(\d+\.\s*(?:\[[^\]]+\]\s*)?[^\n]+?\?\s*(?:\n\s*[A-D]\)\s*[^\n]+){2,5})",
        re.MULTILINE,
    )
 
    matches = mcq_pattern.findall(text)
    mcqs = []
 
    for block in matches:
        lines = [ln.strip() for ln in block.strip().split("\n") if ln.strip()]
        mcqs.append("\n".join(lines))
 
    return mcqs
 
 
def save_mcqs_to_file(mcqs, output_file="mcqs_only.txt"):
    """Saves extracted MCQs to a text file"""
    with open(output_file, "w", encoding="utf-8") as f:
        for mcq in mcqs:
            f.write(mcq + "\n\n")
    print(f"[✅] Filtered MCQs saved to {output_file}")
 
 
 
if __name__ == "__main__":
    pdf_path = r"C:\Users\VibhuDixit\OneDrive - Meridian Solutions\Desktop\PdfMCQ\MCQ_Test_Image_Based_With_Uploaded_Pics.pdf"  # <-- put your PDF path here
 
   
    text = extract_text_from_pdf(pdf_path)
 
   
    with open("output.txt", "r", encoding="utf-8") as f:
        text = f.read()
 
    mcqs = extract_mcqs_from_text(text)
    print(f"[INFO] Found {len(mcqs)} MCQs.")
    save_mcqs_to_file(mcqs)
 