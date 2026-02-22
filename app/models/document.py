from sqlalchemy import  Column,String,Integer,DateTime,Text
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import enum
import uuid

class DocumentStatus(enum.Enum):
    uploaded="uploaded"
    preprocessing="preprocessing"
    completed="completed"
    failed="failed"

class Document(Base):
    __tablename__='documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename= Column(String,nullable=False)
    stored_filename=Column(String,nullable=False)
    size_in_bytes=Column(Integer,nullable=False)
    content_type=Column(String,nullable=False)
    status=Column(Enum(DocumentStatus,name='document_status'),server_default=DocumentStatus.preprocessing.value,nullable=False,index=True)
    upload_time=Column(DateTime,default=datetime.utcnow,index=True,nullable=False)
    content=relationship("DocumentContent", back_populates="document", uselist=False)
    


    

