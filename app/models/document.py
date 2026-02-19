from sqlalchemy import  Column,String,Integer,DateTime,Text
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
import uuid
class Document(Base):
    __tablename__='documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename= Column(String,nullable=False)
    stored_filename=Column(String,nullable=False)
    size_in_bytes=Column(Integer,nullable=False)
    content_type=Column(String,nullable=False)
    upload_time=Column(DateTime,default=datetime.utcnow)
    content=relationship("DocumentContent", back_populates="document", uselist=False)
    


    

