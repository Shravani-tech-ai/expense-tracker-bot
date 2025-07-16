from langchain_core.tools import Tool
from utils.storage import get_expense_summary
import json
from datetime import datetime

def get_summary_handler(input: str) -> str:
    """
    Handler for getting expense summary.
    Input must be a JSON string:
    {
        "period": "week", 
        "category": "food", 
        "specific_date": "2025-05-29"  # Optional
    }
    """
    try:
        data = json.loads(input)
        period = data.get("period", "month")
        category = data.get("category", None)
        specific_date_str = data.get("specific_date", None)
        specific_date = None

        # Convert to datetime object if present
        if specific_date_str:
            specific_date = datetime.strptime(specific_date_str, "%Y-%m-%d")

        return get_expense_summary(period, category, specific_date)
    except Exception as e:
        return f"Error: {str(e)}"

tool_get_summary = Tool(
    name="GetExpenseSummary",
    func=get_summary_handler,
    description=(
        "Use this tool to get a summary of expenses. "
        "Input should be JSON like {\"period\": \"week\", \"category\": \"travel\"}. "
        "'category' and 'specific_date' are optional. Use 'month', 'week', or 'day' as period. "
        "If you want to query a specific date, provide 'specific_date' as YYYY-MM-DD."
    )
)
