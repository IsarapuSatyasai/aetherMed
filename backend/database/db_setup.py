from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from backend.config import settings

# Initialize the engine without the SQLite thread arguments
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()