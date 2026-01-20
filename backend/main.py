import time
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
import requests
import json

from backend.confidence import calculate_confidence
from backend.logger import log_event
from backend.rag.retrieve import retrieve_context
from backend.schemas import MatchAnalysis
from backend.storage import save_analysis

MAX_RETRIES = 2
SYSTEM_PROMPT = """
        You are a JSON generator.

Rules:
1. Output ONLY valid JSON.
2. Do not include any text before or after JSON.
3. Do not explain anything.
4. JSON must exactly match this schema:
{
  "strengths": ["string"],
  "mistakes": ["string"],
  "training_focus": ["string"],
  "confidence": number between 0 and 1
}

    """

def call_my_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]  

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
            1. You MUST return valid JSON.
            2. The JSON MUST match this schema exactly:
                {
                "strengths": ["string"],
                "mistakes": ["string"],
                "training_focus": ["string"],
                "confidence": number between 0 and 1
                }
            3. Do NOT add extra keys.
            4. Do NOT include explanations or markdown.
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

@app.post("/analyze-match-with-rag")
def analyze_match_with_rag(request: MatchRequest):
    retrieval = retrieve_context(request.match_summary)
    log_event("request", {"summary": request.match_summary})
    context = retrieval["context"]
    distances = retrieval["distances"]
    log_event("retrieval", {"distances": distances})

    user_prompt = f"""
Use ONLY the following knowledge:
{context}

Match summary:
{request.match_summary}
"""

    full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    for attempt in range(MAX_RETRIES):
        raw_output = call_my_llm(full_prompt)

        print("\n--- RAW LLM OUTPUT (attempt", attempt + 1, ") ---")
        print(raw_output)

        try:
            parsed = MatchAnalysis.model_validate_json(raw_output)
            log_event("analysis", parsed.model_dump())
            save_analysis(parsed.model_dump())
            
            confidence = calculate_confidence(distances, parsed)
            parsed.confidence = confidence
            return parsed.model_dump()

        except ValidationError as e:
            print("❌ Validation error:", e)


    return {
        "error": "AI failed to produce valid output",
        "confidence": 0.0
    }

@app.post("/feedback")
def feedback(analysis_id: int, useful: bool):
    log_event("feedback", {
        "analysis_id": analysis_id,
        "useful": useful
    })
    return {"status": "recorded"}
