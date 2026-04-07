import os
import shutil
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.embeddings_generator import generate_embedding
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
from backend.database import SessionLocal
from backend.models import Candidate, Job
from backend.resume_parser import pdf_path

app = Flask(__name__)

# Enabling CORS for all routes (Replacing FastAPI middleware)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        missing_skills=", ".join(data["missing"])
    )
    db.add(candidate)
    db.commit()
    db.close()

@app.route("/", methods=["GET"])
def home():
    return render_template('clientside.html')
    # return jsonify({"message": "Resume Intelligence API Running"})

@app.route("/analyze-resume", methods=["POST", "GET"])
def analyze_resume():
    # Flask uses request.files for file uploads
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    # Extract name
    lines = resume_text.split("\n")
    name = "Unknown Candidate"
    for line in lines:
        line = line.strip()
        if len(line) > 3 and "@" not in line:
            name = line
            break

    # NLP Processing
    resume_clean = process_text(resume_text)
    resume_embedding = generate_embedding(resume_clean)

    # Job Description
    # Note: __file__ context remains same as your original script
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    job_path = os.path.join(BASE_DIR,"Thinkathon2026", "data", "jd.txt")

    with open(job_path, "r") as f:
        job_text = f.read()

    job_clean = process_text(job_text)
    job_embedding = generate_embedding(job_clean)

    # Scores
    semantic_score = calculate_similarity(resume_embedding, job_embedding)
    resume_skills = extract_skills(resume_clean)
    job_skills = extract_skills(job_clean)

    skill_score = calculate_skill_score(resume_skills, job_skills)
    experience_score = calculate_experience_score()

    final_score = calculate_final_score(
        semantic_score,
        skill_score,
        experience_score
    )

    missing_skills = get_skill_gap(resume_skills, job_skills)
    category = classify_candidate(final_score, skill_score)

    # Save to Database
    data = {
        "name": name,
        "semantic": float(semantic_score),
        "skill": float(skill_score),
        "experience": float(experience_score),
        "final": float(final_score),
        "category": category,
        "matched": resume_skills,
        "missing": missing_skills
    }
    save_to_db(data)

    # Returning JSON response
    return jsonify({
        "name": name,
        "semantic": round(float(semantic_score), 2),
        "skill": round(float(skill_score), 2),
        "final": round(float(final_score), 2),
        "category": category,
        "missing": missing_skills, 
        "matched": resume_skills
    })

@app.route("/jobs", methods=["GET"])
def get_jobs():
    db = SessionLocal()
    jobs = db.query(Job).all()

    job_list = []
    for job in jobs:
        job_list.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "mandatory_skills": job.mandatory_skills.split(","),
            "optional_skills": job.optional_skills.split(",")
        })
    
    return jsonify(job_list)

if __name__ == "__main__":
    app.run(debug=True, port=8000)