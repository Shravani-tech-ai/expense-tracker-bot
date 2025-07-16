import re
from datetime import date

def parse_bill_text(text: str) -> dict:
    # Clean the text
    clean_text = text.replace("|", "I").replace("\n", " ").strip()
    clean_text = re.sub(r"\s+", " ", clean_text)

    print("🧾 Cleaned Text:", clean_text)

    # Extract amount
    amount_match = re.search(r"\b(?:Rs\.?|₹)?\s?(\d+)\b", clean_text)
    if not amount_match:
        raise ValueError("Could not extract amount.")
    amount = int(amount_match.group(1))

    # Extract category
    category_match = re.search(r"on (\w+)", clean_text)
    if not category_match:
        raise ValueError("Could not extract category.")
    category = category_match.group(1).lower()

    return {
        "amount": amount,
        "category": category,
        "date": str(date.today())
    }
