from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil
import os

from models import Candidate, Job
from database import SessionLocal

from embedding_generator import generate_embedding
from resume_parser import extract_text
from nlp_processor import process_text
from insight_engine import (
    calculate_similarity,
    calculate_experience_score,
    classify_candidate
)
from skill_extractor import extract_skills


# -------------------- APP INIT --------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------- SCHEMA --------------------

class JobCreate(BaseModel):
    title: str
    description: str
    mandatory_skills: List[str]
    optional_skills: List[str]
    certification_enabled: bool
    certification_weight: float


# -------------------- DATABASE SAVE --------------------

def save_to_db(data):
    db = SessionLocal()

    candidate = Candidate(
    name=data["name"],
    semantic_score=data["semantic"],
    skill_score=data["skill"],
    experience_score=data["experience"],
    final_score=data["final"],
    category=data["category"],
    matched_skills=", ".join(data["matched"]),
    missing_skills=", ".join(data["missing"]),
    job_id=data["job_id"],
    eligibility_status=data["eligibility_status"]
)

    db.add(candidate)
    db.commit()
    db.close()


# -------------------- HOME --------------------

@app.get("/")
def home():
    return {"message": "Resume Intelligence API Running"}


# -------------------- CREATE JOB --------------------

@app.post("/create-job")
def create_job(job: JobCreate):

    db = SessionLocal()

    new_job = Job(
        title=job.title,
        description=job.description,
        mandatory_skills=", ".join(job.mandatory_skills),
        optional_skills=", ".join(job.optional_skills),
        certification_enabled=job.certification_enabled,
        certification_weight=job.certification_weight
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    db.close()

    return {
        "message": "Job created successfully",
        "job_id": new_job.id
    }


# -------------------- RESUME ANALYSIS --------------------

@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_id: int = Form(...)
):

    db = SessionLocal()

    # Fetch Job
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        db.close()
        return {"error": "Job not found"}

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    resume_text = extract_text(file_path)

    # Extract name
    lines = resume_text.split("\n")
    name = "Unknown Candidate"

    for line in lines:
        line = line.strip()
        if len(line) > 3 and "@" not in line:
            name = line
            break

    # NLP + Embeddings
    resume_clean = process_text(resume_text)
    resume_embedding = generate_embedding(resume_clean)

    job_text = job.description
    job_clean = process_text(job_text)
    job_embedding = generate_embedding(job_clean)

    # Semantic Score
    semantic_score = calculate_similarity(resume_embedding, job_embedding)

    # -------------------- SMART SKILL SCORING --------------------

    resume_skills = extract_skills(resume_clean)

    mandatory_skills = [s.strip() for s in job.mandatory_skills.split(",")]
    optional_skills = [s.strip() for s in job.optional_skills.split(",")]

    matched_mandatory = [s for s in mandatory_skills if s in resume_skills]
    matched_optional = [s for s in optional_skills if s in resume_skills]

    mandatory_score = len(matched_mandatory) / len(mandatory_skills) if mandatory_skills else 1
    optional_score = len(matched_optional) / len(optional_skills) if optional_skills else 0

    skill_score = (0.7 * mandatory_score) + (0.3 * optional_score)

    # -------------------- CERTIFICATION SCORING --------------------

    certification_score = 0

    if job.certification_enabled:
        text_lower = resume_text.lower()

        if ("certified" in text_lower or 
            "certification" in text_lower or 
            "badge" in text_lower):

            certification_score = 1

        skill_score += certification_score * job.certification_weight

    # -------------------- EXPERIENCE --------------------

    experience_score = calculate_experience_score()

    # -------------------- FINAL SCORE --------------------

    final_score = (
        0.4 * semantic_score +
        0.4 * skill_score +
        0.2 * experience_score
    )

    # -------------------- OUTPUT LOGIC --------------------

    missing_skills = [s for s in mandatory_skills if s not in resume_skills]

    if len(missing_skills) > 0:
        eligibility_status = "Rejected - Missing Mandatory Skills"
    else:
        eligibility_status = "Eligible"

    category = classify_candidate(final_score, skill_score)

    # Save to DB
    data = {
        "name": name,
        "semantic": float(semantic_score),
        "skill": float(skill_score),
        "experience": float(experience_score),
        "final": float(final_score),
        "category": category,
        "matched": matched_mandatory + matched_optional,
        "missing": missing_skills,
        "job_id": job_id,
        "eligibility_status": eligibility_status
    }

    save_to_db(data)
    db.close()

    return {
        "name": name,
        "semantic_score": round(float(semantic_score), 2),
        "skill_score": round(float(skill_score), 2),
        "final_score": round(float(final_score), 2),
        "category": category,
        "missing_skills": missing_skills,
        "eligibility_status": eligibility_status
    }