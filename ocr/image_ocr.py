from PIL import Image
import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if needed

def extract_text_from_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ File not found: {image_path}")

    # Special handling for webp
    if image_path.endswith(".webp"):
        img = Image.open(image_path).convert("RGB")
        image_path = image_path.replace(".webp", ".jpg")
        img.save(image_path, "JPEG")
        print(f"🔄 Converted .webp to .jpg: {image_path}")

    # Load with OpenCV
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"❌ OpenCV couldn't read the image. File may be corrupted or unsupported: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    print("📑 Extracted text:\n", text)
    return text
