from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="Sales Insight Automator")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Sales Insight Automator API running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), email: str = Form(...)):

    df = pd.read_csv(file.file)

    data = df.to_string()

    prompt = f"""
    Analyze the following sales dataset and generate a professional executive summary.

    DATA:
    {data}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        summary = response.text

    except Exception as e:
        summary = "AI service temporarily unavailable. Please try again later."

    return {
        "email": email,
        "summary": summary
    }