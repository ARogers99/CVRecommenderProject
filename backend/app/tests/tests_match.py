from fastapi.testclient import TestClient
from app.main import app
from app.services.matcher import extract_skills, match_score, match_cv_job
from app.models.jobs import Job

client = TestClient(app)


# test the helper functions directly
def test_extract_skills():
    text = "We need experience with Python, FastAPI and Docker"
    skills = extract_skills(text)
    assert "python" in skills
    assert "fastapi" in skills
    assert "docker" in skills


def test_extract_skills_case_insensitive():
    text = "Experience with PYTHON and React required"
    skills = extract_skills(text)
    assert "python" in skills
    assert "react" in skills


def test_match_score_perfect_score():
    cv_skills = ["python", "fastapi", "docker"]
    job_skills = ["python", "fastapi", "docker"]
    assert match_score(cv_skills, job_skills) == 1.0


def test_match_score_no_score():
    cv_skills = ["python", "fastapi"]
    job_skills = ["java", "spring"]
    assert match_score(cv_skills, job_skills) == 0.0


def test_match_score_no_skills():
    cv_skills = ["python"]
    job_skills = []
    assert match_score(cv_skills, job_skills) == 0.0


def test_match_cv_filters_low_scores():
    jobs = [
        Job(job_id="1", title="Python Dev", company="Corp", location="Dublin",
            description="python fastapi docker", link="http://test.com"),
        Job(job_id="2", title="Java Dev", company="Corp", location="Dublin",
            description="java spring hibernate", link="http://test.com")
    ]
    cv_text = "experienced python and fastapi developer"
    result = match_cv_job(cv_text, jobs)

    # java job should be filtered out
    assert all(m.score > 0.2 for m in result.matches)


def test_match_cv_sorted_by_score():
    jobs = [
        Job(job_id="1", title="Python Dev", company="Corp", location="Dublin",
            description="python fastapi docker aws", link="http://test.com"),
        Job(job_id="2", title="Senior Python Dev", company="Corp", location="Dublin",
            description="python", link="http://test.com")
    ]
    cv_text = "python fastapi docker aws developer"
    result = match_cv_job(cv_text, jobs)

    # first result should have higher score
    if len(result.matches) > 1:
        assert result.matches[0].score >= result.matches[1].score