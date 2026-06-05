import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200

def test_upload_valid_pdf():
    test_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(test_dir, "sample_cv.pdf")

    with open(pdf_path, "rb") as f:
        file_data = f.read()
    response = client.post(
        "/cv/upload",
        files={"file": ("cv.pdf", file_data, "application/pdf")}
    )

    assert response.status_code == 200
    assert response.json()["raw_text"] != ""