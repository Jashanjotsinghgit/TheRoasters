SKILLS = [
    "python", "java", "sql", "machine learning",
    "deep learning", "django", "mysql",
    "numpy", "pandas", "scikit", "llm",
    "prompt engineering", "git", "github"
]

def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill in text.lower():
            found.append(skill)

    return found