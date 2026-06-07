from anthropic.resources.beta.skills import skills
from pypdfium2_cli import extract_text

from app.models.jobs import Job
from app.models.match import JobMatch, MatchResponse

SKILLS = ["python", "javascript", "typescript", "java", "sql", "react", "fastapi",
    "django", "flask", "docker", "aws", "git", "postgresql", "mongodb",
    "machine learning", "pytorch", "scikit-learn", "pandas", "opencv",
    "node", "css", "html", "kubernetes", "ci/cd", "rest api"]

def extract_skills(text:str) -> list[str]:
    text = text.lower()

    return [skill for skill in SKILLS if skill in text]

def match_score(cv_skills: list[str], job_skills:list[str]) -> float:
    if not job_skills:
        return 0.0
    matching = set(job_skills) & set(cv_skills)
    score = round(len(matching) / len(job_skills), 2)
    return score

def match_cv_job(cv_text: str, jobs: list[Job]) -> MatchResponse:
    cv_skills = extract_skills(cv_text)

    matches = []
    for job in jobs:
        job_skills = extract_skills(job.description)
        matching_skills = list(set(job_skills) & set(cv_skills))
        missing_skills = list(set(job_skills) - set(cv_skills))
        score = match_score(cv_skills, job_skills)

        matches.append(JobMatch(job = job, matching_skills=matching_skills, missing_skills=missing_skills,
                              score=score))
    matches = sorted(matches, key=lambda match: match.score, reverse=True)
    matches = [m for m in matches if m.score > 0.1]
    return MatchResponse(matches=matches, total=len(matches))


