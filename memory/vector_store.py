import os
import re
import traceback
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Setup paths
DB_DIR = os.path.join(os.path.dirname(__file__), "vector_db")
INDEX_FILE = os.path.join(DB_DIR, "index.faiss")
DOCS_FILE = os.path.join(DB_DIR, "docs.json")
os.makedirs(DB_DIR, exist_ok=True)

# Debug info
print("📂 VECTOR DB DIR:", DB_DIR)
print("📄 INDEX FILE:", INDEX_FILE)
print("📝 DOCS FILE:", DOCS_FILE)

# Load local embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_db():
    print(f"🔍 Checking for FAISS index at: {INDEX_FILE}")
    if os.path.exists(INDEX_FILE) and os.path.exists(DOCS_FILE):
        print("📦 FAISS DB found. Loading...")
        db = FAISS.load_local(DB_DIR, embedding_model, allow_dangerous_deserialization=True)
        print(f"✅ FAISS loaded. Documents: {len(db.docstore._dict)}")
        return db
    else:
        print("🆕 No FAISS DB found. Will create new on first doc.")
        return None

def save_db(db):
    try:
        db.save_local(DB_DIR)
        print("💾 Vector DB saved.")
    except Exception as e:
        print(f"❌ Failed to save FAISS DB: {e}")

def add_expense_doc(expense_entry: dict):
    try:
        for key in ["amount", "category", "date"]:
            if key not in expense_entry:
                raise ValueError(f"Missing key: {key}")

        content = f"{expense_entry['category']} ₹{expense_entry['amount']} on {expense_entry['date']}"
        print("📄 Vector entry to add:", content)

        doc = Document(page_content=content, metadata=expense_entry)
        db = get_db()

        if db:
            db.add_documents([doc])
        else:
            db = FAISS.from_documents([doc], embedding_model)

        save_db(db)
        print("✅ Document added to vector store.")

    except Exception:
        print("❌ Failed to add to FAISS:")
        traceback.print_exc()

def extract_category_from_query(query: str) -> str:
    """Extracts the category from user query using simple NLP."""
    match = re.search(r"(?:for|on|under)\s+(\w+)", query.lower())
    return match.group(1) if match else ""

def query_expenses(query: str, k=3):
    try:
        db = get_db()
        if not db:
            print("📂 Vector DB is empty. No entries yet.")
            return []

        target_category = extract_category_from_query(query)
        print(f"🎯 Looking for category: {target_category}")

        results = db.similarity_search(query, k=k)
        print(f"🔍 Query: {query}, Results: {len(results)}")

        # Optional filtering by category
        filtered = [r for r in results if r.metadata.get("category") == target_category]
        print(f"✅ Filtered Results: {len(filtered)}")

        return filtered

    except Exception as e:
        print(f"❌ Vector search error: {e}")
        return []
