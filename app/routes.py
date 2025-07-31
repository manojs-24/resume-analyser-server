from fastapi import UploadFile, File, APIRouter, Form
from app.schemas import  SuccessResponse, ErrorResponse
from datetime import datetime
from app.gemini import summarize_resume, ats_score_by_role
import fitz  # PyMuPDF

router = APIRouter()

# ✅ Root route
@router.get("/", response_model=SuccessResponse)
def root():
    return SuccessResponse(
        message= "Welcome to Gemini Resume Summary API",
        data={"data": "Hii !"},
        timestamp=datetime.utcnow()
    ).to_response()


# ✅ Health check route
@router.get("/health", response_model=SuccessResponse)
def health_check():
    return SuccessResponse(
        message= "Server is healthy.",
        data={"status": "ok"},
        timestamp=datetime.utcnow()
    ).to_response()



@router.post("/generate-summary")
async def generate_summary(file: UploadFile = File(...)):
    try:
        # ✅ Read and save file
        content = await file.read()
        with open("resume.pdf", "wb") as f:
            f.write(content)

        # ✅ Extract text
        doc = fitz.open("resume.pdf")
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()

        # ✅ Generate summary from extracted text
        summary = await summarize_resume(resume_text)

        return SuccessResponse(
            data={"summary": summary},
            timestamp=datetime.utcnow()
        ).to_response()

    except Exception as e:
        return ErrorResponse(
            error=str(e),
            message="Failed to generate summary",
            timestamp=datetime.utcnow()
        ).to_response(status_code=500)
    

@router.post("/ats-score")
async def analyze_ats_score(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    try:
        content = await file.read()
        with open("resume.pdf", "wb") as f:
            f.write(content)

        doc = fitz.open("resume.pdf")
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()
        # print(resume_text)

        score_feedback = await ats_score_by_role(resume_text, role)

        return SuccessResponse(
            data={
                "role_checked": role,
                "result": score_feedback
            },
            timestamp=datetime.utcnow()
        ).to_response()

    except Exception as e:
        return ErrorResponse(
            error=str(e),
            message="Failed to calculate ATS score",
            timestamp=datetime.utcnow()
        ).to_response(status_code=500)


