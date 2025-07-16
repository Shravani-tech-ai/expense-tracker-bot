from db.models import Expense, SessionLocal
from datetime import datetime, timedelta
from memory.vector_store import add_expense_doc

def add_expense(*args, **kwargs):
    """
    Supports both:
    - add_expense(expense_dict)
    - add_expense(amount, category, date)
    """
    session = SessionLocal()
    try:
        # Handle dictionary input
        if len(args) == 1 and isinstance(args[0], dict):
            expense = args[0]
            amount = expense["amount"]
            category = expense["category"]
            date_str = expense.get("date")
        # Handle positional arguments
        elif len(args) == 3:
            amount, category, date_str = args
        else:
            raise ValueError("Invalid input format to add_expense")

        # Convert to datetime.date or fallback to today
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.today().date()

        # Store in PostgreSQL
        db_entry = Expense(amount=amount, category=category, date=date_obj)
        session.add(db_entry)
        session.commit()

        # Add to FAISS vector DB
        add_expense_doc({
            "amount": amount,
            "category": category,
            "date": str(date_obj)
        })

        return f"✅ Added ₹{amount} under {category} on {date_obj}"

    except Exception as e:
        session.rollback()
        return f"❌ Error: {e}"

    finally:
        session.close()


def get_expense_summary(period, category=None, specific_date=None):
    """
    Retrieves the total expense summary based on period and optional filters.
    """
    session = SessionLocal()
    try:
        query = session.query(Expense)

        if category:
            query = query.filter(Expense.category == category)

        if specific_date:
            query = query.filter(Expense.date == specific_date)

        elif period == "day":
            today = datetime.today().date()
            query = query.filter(Expense.date == today)

        elif period == "week":
            today = datetime.today().date()
            start_week = today - timedelta(days=today.weekday())
            query = query.filter(Expense.date >= start_week)

        elif period == "month":
            today = datetime.today()
            query = query.filter(Expense.date >= today.replace(day=1).date())

        total = sum(e.amount for e in query.all())
        return f"📊 Total spent{f' on {category}' if category else ''} this {period}: ₹{total}"

    except Exception as e:
        return f"❌ Error: {e}"

    finally:
        session.close()
