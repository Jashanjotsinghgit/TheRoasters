from sentence_transformers import SentenceTransformer
from backend.resume_parser import extract_text
from backend.nlp_processor import process_text
from backend.insight_engine import (
    calculate_similarity,
    calculate_skill_score,
    calculate_experience_score,
    calculate_final_score,
    get_skill_gap,
    classify_candidate
)
from backend.skill_extractor import extract_skills
from backend.resume_parser import pdf_path 

import os
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    return model.encode(text)

from backend.database import SessionLocal
from backend.models import Candidate

def save_to_db(data):

    db = SessionLocal()

    # Check if already exists
    existing = db.query(Candidate).filter(
        Candidate.name == data["name"],
        Candidate.final_score == data["final"]
    ).first()

    if existing:
        print("Duplicate entry found. Not saving again.")
        db.close()
        return

    candidate = Candidate(
        name=data["name"],
        semantic_score=data["semantic"],
        skill_score=data["skill"],
        experience_score=data["experience"],
        final_score=data["final"],
        category=data["category"],
        matched_skills=", ".join(data["matched"]),
        missing_skills=", ".join(data["missing"])
    )

    db.add(candidate)
    db.commit()
    db.close()


if __name__ == "__main__":

    resume_path = pdf_path

    # Resume
    resume_text = extract_text(resume_path)

    lines = resume_text.split("\n")

    name = "Unknown Candidate"

    for line in lines:
        line = line.strip()

        if len(line) > 3 and "@" not in line and "http" not in line:
            name = line
            break
      
    resume_clean = process_text(resume_text)
    resume_embedding = generate_embedding(resume_clean)

    # Job Description
   
    BASE_DIR = os.path.dirname(__file__)
    job_path = os.path.join(BASE_DIR, "data", "jd.txt")
    print(BASE_DIR)
    print(job_path)

    with open(job_path, "r") as f:
        job_text = f.read()

    job_clean = process_text(job_text)
    job_embedding = generate_embedding(job_clean)

    # Semantic Score
    semantic_score = calculate_similarity(
        resume_embedding,
        job_embedding
    )

    # Skill Score
    resume_skills = extract_skills(resume_clean)
    job_skills = extract_skills(job_clean)

    skill_score = calculate_skill_score(
        resume_skills,
        job_skills
    )

    # Experience Score
    experience_score = calculate_experience_score()

    # Final Score
    final_score = calculate_final_score(
        semantic_score,
        skill_score,
        experience_score
    )

    # Skill Gap
    missing_skills = get_skill_gap(
    resume_skills,
    job_skills
    )

    # Classification
    category = classify_candidate(final_score, skill_score)

    data = {
    "name" : name,
    "semantic": semantic_score,
    "skill": skill_score,
    "experience": experience_score,
    "final": final_score,
    "category": category,
    "matched": resume_skills,
    "missing": missing_skills
}

    try:
      save_to_db(data)
      print("Data saved to database successfully")
    except Exception as e:
       print("Database error:", e)

    # Output
    print("\n--- FINAL ANALYSIS ---")

    print("\nSemantic Score:", round(semantic_score, 2))
    print("Skill Score:", round(skill_score, 2))
    print("Experience Score:", experience_score)

    print("\nFinal Score:", round(final_score, 2))
    print("Final Match %:", round(final_score * 100, 2), "%")

    print("\nCategory:", category)

    print("\nMatched Skills:", resume_skills)
    print("Required Skills:", job_skills)
    print("Missing Skills:", missing_skills)