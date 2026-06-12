from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import cv, jobs, match, suggestions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.router)
app.include_router(jobs.router)
app.include_router(match.router)
app.include_router(suggestions.router)

@app.get("/")
async def root():
    return {"message": "CV Recommender API"}