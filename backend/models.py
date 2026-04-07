# from sqlalchemy import Column, Integer, Float, String, Text
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Candidate(Base):

#     __tablename__ = "candidates"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     semantic_score = Column(Float)
#     skill_score = Column(Float)
#     experience_score = Column(Float)
#     final_score = Column(Float)
#     category = Column(String)
#     matched_skills = Column(Text)
#     missing_skills = Column(Text)

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    mandatory_skills = Column(String)
    optional_skills = Column(String)
    certification_enabled = Column(Boolean, default=False)
    certification_weight = Column(Float, default=0.0)

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
    eligibility_status = Column(String)
    job_id = Column(Integer, ForeignKey("jobs.id"))