import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {"Content-Type": "application/json"}

async def summarize_resume(resume_text: str) -> str:
    prompt = f"""
You are a professional resume analyst and career advisor.

1. Carefully review the following resume.
2. Write a **detailed professional summary** (at least 8 lines) highlighting the candidate's skills, experience, and strengths.
3. Based on the resume, suggest **3-5 job roles or titles** the candidate is well-suited for in the current market.

Resume:
{resume_text}
"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(f"{GEMINI_URL}?key={API_KEY}", headers=HEADERS, json=payload)
            response.raise_for_status()
            content = response.json()
            return content["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print("❌ Summary generation failed:", str(e))
            raise e



async def ats_score_by_role(resume_text: str, target_role: str) -> str:
    prompt = f"""
You are an Applicant Tracking System (ATS) simulator.

Compare the following resume against the role: "{target_role}".

Give your response in **JSON format** like this:
{{
  "score": <integer between 0 and 100>,
  "points": [
    "<reason or observation>",
    "<reason or observation>",
    ...
  ]
}}

The score should reflect how well the resume matches the job role based on skills, keywords, and formatting. Include both positive and negative points if needed.

Resume:
{resume_text}
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(f"{GEMINI_URL}?key={API_KEY}", headers=HEADERS, json=payload)
            response.raise_for_status()
            content = response.json()
            return content["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print("❌ Summary generation failed:", str(e))
            raise e
