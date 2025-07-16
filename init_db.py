# init_db.py

from db.models import create_tables

if __name__ == "__main__":
    create_tables()
    print("✅ Tables created successfully.")
