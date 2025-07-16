# memory/memory_manager.py

import os
import json
from datetime import datetime

def store_to_memory(entry: dict, user_id: str = "default_user"):
    os.makedirs("data", exist_ok=True)
    filename = f"data/memory_{user_id}.json"

    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
        else:
            data = []

        entry["_timestamp"] = datetime.now().isoformat()
        data.append(entry)

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ Memory store error: {e}")

def load_memory(user_id: str = "default_user"):
    filename = f"data/memory_{user_id}.json"
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return []
