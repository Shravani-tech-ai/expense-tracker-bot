from langchain_core.tools import Tool
from utils.storage import add_expense
import json

def add_expense_handler(input: str) -> str:
    """
    Handler for adding an expense. Input must be a JSON string:
    {"amount": 200, "category": "rent", "date": "2024-07-01"}
    """
    try:
        data = json.loads(input)
        if "amount" not in data or "category" not in data:
            return "Error: 'amount' and 'category' are required."
        return add_expense(data)  # ✅ send as dictionary
    except Exception as e:
        return f"Error: {str(e)}"

tool_add_expense = Tool(
    name="AddExpense",
    func=add_expense_handler,
    description=(
        "This tool adds a new expense record. Required JSON input: "
        '{"amount": int, "category": str, "date": "YYYY-MM-DD" (optional)}.'
        "Example: {\"amount\": 500, \"category\": \"rent\"}"
    )
)
