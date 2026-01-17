import requests

url = "http://localhost:11434/api/generate"

payload={
    "model": "llama3",
    "prompt": "what is the weather like in Gurugram?",
    "stream": False
}

response = requests.post(url, json=payload)
print(response.json()["response"])
