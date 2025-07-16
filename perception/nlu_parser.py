import re
from datetime import datetime
from dateparser.search import search_dates

def parse_input(user_input: str) -> dict:
    user_input = user_input.strip().lower()

    # 🔍 Match recall queries (when did, last time, previous, recent...)
    if any(q in user_input for q in ["when did", "last time", "previous", "recent"]):
        return {
            "intent": "recall_expense",
            "query": user_input
        }

    # 🧠 Match natural language expense: "I spent 200 on food today" or "for food"
    match = re.search(r"spent\s*(\d+)\s*(?:on|for)?\s*([\w\s]+)", user_input)
    if match:
        amount = int(match.group(1))
        raw_category = match.group(2).strip()

        noisy_keywords = ["today", "yesterday", "this", "week", "month", "day"]
        category_words = [
            word for word in raw_category.split()
            if word not in noisy_keywords and not re.match(r"\d{4}", word)
        ]
        category = category_words[0] if category_words else "misc"

        date_found = search_dates(user_input, settings={'PREFER_DATES_FROM': 'past'})
        if date_found:
            parsed_date = date_found[0][1]
            if parsed_date.year >= 2000:
                date_str = parsed_date.strftime("%Y-%m-%d")
            else:
                date_str = datetime.today().strftime("%Y-%m-%d")
        else:
            date_str = datetime.today().strftime("%Y-%m-%d")

        return {
            "intent": "add_expense",
            "amount": amount,
            "category": category,
            "date": date_str,
        }

    # 🧾 Match structured input: amount=200, category=food, date=2024-07-01
    if "amount=" in user_input and "category=" in user_input:
        pattern = r'(\w+)=("[^"]*"|\'[^\']*\'|[^,]+)'
        matches = re.findall(pattern, user_input)
        data = {}
        for key, value in matches:
            value = value.strip().strip("\"'")
            if key == "amount":
                data[key] = int(value)
            else:
                data[key] = value
        return {
            "intent": "add_expense",
            **data
        }

    # 📊 Match summary queries
    periods = {"today": "day", "day": "day", "week": "week", "month": "month"}
    period = "month"
    for keyword, value in periods.items():
        if keyword in user_input:
            period = value
            break

    categories = ["rent", "food", "groceries", "travel", "shopping", "entertainment"]
    category = next((c for c in categories if c in user_input), None)

    return {
        "intent": "get_summary",
        "period": period,
        "category": category
    }
