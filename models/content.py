from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import relationship

from . import Base


# Content table
class Content(Base):
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    page_number = Column(Integer, index=True)
    text_content = Column(Text)
    image_content = Column(Text, nullable=True)

    # Establish relationship with Document
    document = relationship("Document", back_populates="contents")