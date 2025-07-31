from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gemini Resume Analyser")

app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow everything during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)