from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

class MatchRequest(BaseModel):
    match_summary: str

@app.post("/analyze-match")
def analyze_match(request: MatchRequest):
    system_prompt = """
        You are a professional badminton coach.

        Rules:
        1. Be concise and factual.
        2. Do not make up statistics.
        3. Base advice on amateur-level play.
        4. Output ONLY valid JSON. No markdown, no explanations.
    """
    user_prompt = f"""
        Match Summary:
        {request.match_summary}

        Return JSON in this format only:
        {{
        "strengths": [],
        "mistakes": [],
        "training_focus": []
        }}
    """

    payload = {
        "model": MODEL,
        "prompt": system_prompt + "\n\n" + user_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    raw_output = response.json()["response"]

    try:
        parsed_output = json.loads(raw_output)
    except Exception:
        return {
            "error": "Invalid AI output",
            "raw_output": raw_output
        }

    return parsed_output
