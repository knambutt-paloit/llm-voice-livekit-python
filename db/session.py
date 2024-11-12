# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DATABASE_URL
from models import Base

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory and scoped session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Initialize the database with all tables
def init_db():
    Base.metadata.create_all(bind=engine)