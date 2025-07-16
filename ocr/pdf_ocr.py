import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

def extract_text_from_pdf(pdf_path):
    # Basic file checks
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
        raise ValueError(f"❌ File is missing or empty: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise ValueError(f"❌ PDF loading failed: {e}")

    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {page_num + 1} ---\n{text}"

    return full_text.strip()
