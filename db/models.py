# db/models.py

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date)

# Setup DB connection
DATABASE_URL = "postgresql://shravi_user:Shravani#22@localhost:5432/expense_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
