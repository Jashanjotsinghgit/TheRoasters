from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///resume.db")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)