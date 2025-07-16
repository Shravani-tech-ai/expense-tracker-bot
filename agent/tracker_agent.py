from tools.expense_add import tool_add_expense
from tools.expense_summary import tool_get_summary
from perception.nlu_parser import parse_input
from memory.vector_store import query_expenses
import json

def invoke_agent(user_input: str) -> str:
    parsed = parse_input(user_input)

    if parsed["intent"] == "add_expense":
        payload = {
            "amount": parsed["amount"],
            "category": parsed["category"],
        }
        if parsed.get("date"):
            payload["date"] = parsed["date"]

        return tool_add_expense.invoke(json.dumps(payload))

    elif parsed["intent"] == "get_summary":
        payload = {
            "period": parsed["period"]
        }
        if parsed.get("category"):
            payload["category"] = parsed["category"]

        return tool_get_summary.invoke(json.dumps(payload))

    elif parsed["intent"] == "recall_expense":
        results = query_expenses(parsed["query"])
        if not results:
            return "📭 No similar past expenses found."
        
        output = "🔍 Matching past expenses:\n"
        for doc in results:
            meta = doc.metadata
            output += f"• ₹{meta['amount']} on {meta['category']} ({meta['date']})\n"
        return output.strip()

    return "❌ Sorry, I couldn't understand your request."
