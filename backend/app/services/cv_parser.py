import pdfplumber
import io
from fastapi import UploadFile
from app.models.cv import CVData


async def parse_cv(file: UploadFile) -> CVData:
    contents = await file.read()

    # wrap bytes in a file-like object for pdfplumber
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        raw_text = ""
        for page in pdf.pages:
            raw_text += page.extract_text() or ""

    return CVData(raw_text=raw_text)