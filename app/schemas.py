from pydantic import BaseModel
from typing import Any, Optional, List
from datetime import datetime
from fastapi.responses import JSONResponse


class ResumeInput(BaseModel):
    name: str
    role: str
    skills: List[str]
    experience: str
    education: str

class SummaryResponse(BaseModel):
    summary: str

class SuccessResponse(BaseModel):
    success: bool = True
    message: Optional[str] = "Success"
    data: Any
    timestamp: datetime

    def to_response(self, status_code: int = 200) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": self.success,
                "message": self.message,
                "data": self.data,
                "timestamp": self.timestamp.isoformat()  # ✅ convert to string
            }
        )


class ErrorResponse(BaseModel):
    success: bool = False
    message: Optional[str] = "Internal Server Error"
    error: Any
    timestamp: datetime

    def to_response(self, status_code: int = 500) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": self.success,
                "message": self.message,
                "error": self.error,
                "timestamp": self.timestamp.isoformat()  # ✅ convert to string
            }
        )