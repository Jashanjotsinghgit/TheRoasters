from sqlalchemy import Column, Integer, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Candidate(Base):

    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    semantic_score = Column(Float)
    skill_score = Column(Float)
    experience_score = Column(Float)
    final_score = Column(Float)
    category = Column(String)
    matched_skills = Column(Text)
    missing_skills = Column(Text)

    