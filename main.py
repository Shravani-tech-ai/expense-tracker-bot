import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent.tracker_agent import invoke_agent

print("💰 Expense Tracker Tool (type 'exit' to quit)")
print("Tip: e.g. I spent 300 on food today / amount=500, category=rent")

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break

    try:
        result = invoke_agent(user_input)
        print("🤖", result)
    except Exception as e:
        print("❌ Error:", e)
