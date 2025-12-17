from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_hash = Column(String, unique=True, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    num_chunks = Column(Integer, default=0)
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(Text, nullable=True)
