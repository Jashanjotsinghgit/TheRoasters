from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_emb, job_emb):

    return cosine_similarity(
        [resume_emb],
        [job_emb]
    )[0][0]

# Skill Score
def calculate_skill_score(resume_skills, job_skills):

    if len(job_skills) == 0:
        return 0

    match = 0

    for skill in job_skills:
        if skill in resume_skills:
            match += 1

    return match / len(job_skills)


# Experience Score (basic for now)
def calculate_experience_score():

    # since you are student → fixed value
    return 0.6


# Final Score
def calculate_final_score(semantic, skill, experience):

    final = (
        0.5 * semantic +
        0.3 * skill +
        0.2 * experience
    )

    return final
# Skill Gap
def get_skill_gap(resume_skills, job_skills):

    missing = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)

    return missing

# Classifying candidates as strong, moderate and weak match
def classify_candidate(final_score, skill_score):

    if skill_score >= 0.9:
        return "Strong Match"

    elif final_score >= 0.7:
        return "Strong Match"

    elif final_score >= 0.5:
        return "Moderate Match"

    else:
        return "Weak Match"