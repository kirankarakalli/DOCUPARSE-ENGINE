from sqlalchemy import JSON, UUID, Text,Column,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
import uuid
class DocumentContent(Base):
    __tablename__='document_content'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id=Column(UUID(as_uuid=True),ForeignKey("documents.id"),nullable=False)
    extracted_text = Column(Text, nullable=False)
    structured_data= Column(JSON,nullable=False)

    document = relationship("Document", back_populates="content")

