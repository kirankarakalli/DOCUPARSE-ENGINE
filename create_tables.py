from app.database import engine, Base
from app.models.document import Document
from app.models.document_content import DocumentContent

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
