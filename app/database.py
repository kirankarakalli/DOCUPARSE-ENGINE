from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config.configuration import read_yaml
from sqlalchemy.orm import Session
try:
    config=read_yaml('params.yaml')
except Exception as e:
    raise ValueError(f"Failed to read configuration file: {e}")
DATABASE_URL=config.get('database_url')
if not DATABASE_URL:
    raise ValueError("database_url not found in configuration")

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
Base=declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
