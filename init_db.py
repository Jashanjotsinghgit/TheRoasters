from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Job
import os

# 🔥 DB path
DB_FILE = "resume.db"
DATABASE_URL = f"sqlite:///{DB_FILE}"

# 🔥 DELETE OLD DB (for fresh schema)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Old database deleted.")

# 🔥 Create engine
engine = create_engine(DATABASE_URL)

# 🔥 Create tables
Base.metadata.create_all(engine)
print("New tables created.")

# 🔥 Create session
Session = sessionmaker(bind=engine)
session = Session()

# 🔥 Predefined Jobs
jobs = [
    Job(
        title="Machine Learning Engineer",
        description="Build ML models and deploy AI solutions.",
        mandatory_skills="Python,Machine Learning,Django,MySQL,NumPy,Pandas,Scikit-learn",
        optional_skills="LLM,Prompt Engineering,Git,GitHub",
        certification_enabled=True,
        certification_weight=0.2
    ),
    Job(
        title="Frontend Developer",
        description="Develop modern UI using React and JavaScript.",
        mandatory_skills="HTML,CSS,JavaScript,React",
        optional_skills="Redux,Tailwind,TypeScript",
        certification_enabled=False,
        certification_weight=0.0
    ),
    Job(
        title="Backend Developer",
        description="Work with APIs, databases, and server logic.",
        mandatory_skills="Python,Flask,SQL,REST API",
        optional_skills="Docker,AWS,CI/CD",
        certification_enabled=True,
        certification_weight=0.1
    )
]

# 🔥 Insert data
session.add_all(jobs)
session.commit()

print("Dummy jobs inserted successfully!")

# 🔥 Verify
for job in session.query(Job).all():
    print(job.id, job.title)

session.close()