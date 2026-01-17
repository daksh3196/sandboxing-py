import requests
import json

url = "http://localhost:11434/api/generate"

system_prompt = """
You are a professional badminton coach.

Rules:
1. Be concise and factual.
2. Do not make up statistics.
3. Base advice on amateur-level play.
4. Output must follow the given JSON schema exactly.
5. Output ONLY valid JSON. No explanations. No markdown.
"""

user_prompt = """
Match summary:
- Lost points mainly on backhand defense
- Often cleared under pressure
- Fatigued in long rallies

Return JSON in this format only:
{
  "strengths": [],
  "mistakes": [],
  "training_focus": []
}
"""

payload = {
    "model": "llama3",
    "prompt": system_prompt + "\n\n" + user_prompt,
    "stream": False
}

response = requests.post(url, json=payload)
output = response.json()["response"]

print("RAW OUTPUT:\n", output)

# Optional sanity check
try:
    parsed = json.loads(output)
    print("\nPARSED JSON:\n", parsed)
except Exception as e:
    print("\n⚠️ Output is not valid JSON:", e)
