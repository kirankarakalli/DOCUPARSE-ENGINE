from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config.configuration import read_yaml
from sqlalchemy.orm import Session
config=read_yaml('params.yaml')
DATABASE_URL=config.get('database_url')

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=False,expire_on_commit=False)
Base=declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
