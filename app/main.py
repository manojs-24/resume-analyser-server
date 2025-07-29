from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Gemini Resume Analyser")

app.include_router(router)
