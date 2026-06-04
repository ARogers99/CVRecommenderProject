from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.cv import CVData
from app.services.cv_parser import parse_cv

router = APIRouter(prefix="/cv", tags=["cv"])


@router.post("/upload", response_model=CVData)
async def upload_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        cv_data = await parse_cv(file)
        return cv_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse CV: {str(e)}")