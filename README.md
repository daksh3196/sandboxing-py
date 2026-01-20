# 🏸 OpenCoach Badminton — AI Backend (RAG-Based)

OpenCoach Badminton is a **production-style AI backend** that analyzes badminton match summaries and returns **grounded, structured coaching insights** using a **local LLM + Retrieval-Augmented Generation (RAG)** pipeline.

The project is intentionally backend-focused and demonstrates **AI Software Engineering best practices**, not prompt-level demos.

---

## 🎯 What the System Does

Given a badminton match summary, the backend:

- Retrieves relevant badminton knowledge (rules, tactics, drills)
- Generates structured coaching insights using a local LLM
- Grounds responses using RAG to reduce hallucination
- Validates all AI outputs against strict schemas
- Engineers a deterministic confidence score
- Retries on invalid output and fails safely
- Logs the full AI request lifecycle
- Persists analyses for future evaluation

Everything runs **locally and free**, without paid APIs.

---

## 🧠 Design Philosophy

> **LLMs are non-deterministic dependencies.  
> Software engineers must make them safe.**

Accordingly, this system:
- never trusts raw LLM output
- enforces explicit contracts
- separates knowledge, reasoning, and validation
- prioritizes observability and explainability

---

## ▶️ How to Run the Project (Local)

This backend runs **fully locally** using a local LLM (via Ollama).  
No paid APIs or cloud services are required.

---

### 1️⃣ Prerequisites

Ensure you have the following installed:

- **Python 3.10+**
- **Git**
- **Ollama** (local LLM runtime)

Install Ollama from:
https://ollama.com

Verify installation:
```bash
ollama --version

Pull a local model (once):
ollama run llama3

2. Clone the Repository
git clone https://github.com/daksh3196/sandboxing-py.git
cd opencoach-badminton

3. Create and Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
4. Install Dependencies
pip install -r requirements.txt

5. Index the Knowledge Base (One-Time Step)

This creates vector embeddings for the badminton knowledge base.
python backend/rag/index_kb.py
You should see:

Knowledge base indexed

6. Start the Backend Server
uvicorn backend.main:app --reload


The API will be available at:

http://127.0.0.1:8000

7. Test the API

Open Swagger UI:

http://127.0.0.1:8000/docs


Use the POST /analyze-match-with-rag endpoint with:

{
  "match_summary": "Lost many points on backhand defense and cleared too often under pressure."
}

8. Expected Response
{
  "strengths": ["Good rally endurance"],
  "mistakes": ["Weak backhand defense under pressure"],
  "training_focus": ["Backhand defense drills", "Shot selection under pressure"],
  "confidence": 0.81
}