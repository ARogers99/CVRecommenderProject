from app.models.jobs import Job
from app.models.match import JobMatch, MatchResponse
import re

SKILL_ALIASES = {
    # Languages
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c#": ["c#", "c sharp"],
    "c++": ["c++", "cpp"],
    "sql": ["sql"],

    # Frontend
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular"],
    "vue": ["vue", "vue.js", "vuejs"],
    "next.js": ["next.js", "nextjs", "next"],
    "html": ["html"],
    "css": ["css"],
    "tailwind": ["tailwind", "tailwind css"],

    # Backend
    "fastapi": ["fastapi", "fast api"],
    "django": ["django"],
    "flask": ["flask"],
    "spring": ["spring", "spring boot"],
    ".net": [".net", "dotnet", "asp.net"],
    "node": ["node", "node.js", "nodejs"],
    "express": ["express", "express.js"],
    "rest api": ["rest api", "restful api", "restful", "api development"],
    "graphql": ["graphql"],

    # Databases
    "postgresql": ["postgresql", "postgres", "postgres sql"],
    "mysql": ["mysql"],
    "sql server": ["sql server", "microsoft sql server", "mssql"],
    "mongodb": ["mongodb", "mongo db"],
    "redis": ["redis"],

    # Cloud / DevOps
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "terraform": ["terraform"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment"],
    "linux": ["linux"],

    # Testing / Process
    "testing": ["testing", "unit testing", "automated testing"],
    "pytest": ["pytest"],
    "junit": ["junit"],
    "tdd": ["tdd", "test driven development"],
    "agile": ["agile", "scrum"],

    # Data / ML
    "machine learning": ["machine learning", "ml"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "data analysis": ["data analysis", "data analytics"],
    "nlp": ["nlp", "natural language processing"],
}

def extract_skills(text: str) -> list[str]:
    """

    :rtype: list[str]
    """
    text = text.lower()
    found_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"

            if re.search(pattern, text):
                found_skills.append(canonical_skill)
                break

    return sorted(found_skills)

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
        job_skills = extract_skills(job.description or "")
        matching_skills = list(set(job_skills) & set(cv_skills))
        missing_skills = list(set(job_skills) - set(cv_skills))
        score = match_score(cv_skills, job_skills)

        matches.append(JobMatch(job = job, matching_skills=matching_skills, missing_skills=missing_skills,
                              score=score))
    matches = sorted(matches, key=lambda match: match.score, reverse=True)
    matches = [m for m in matches if m.score > 0.2]
    return MatchResponse(matches=matches, total=len(matches))


