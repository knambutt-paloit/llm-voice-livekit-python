# your_project/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base  # Import the shared Base class


# Document table
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    file_path = Column(String, unique=True, index=True)
    upload_date = Column(String)  # Can store as a timestamp or string

    # Relationship to content table
    contents = relationship("Content", back_populates="document")