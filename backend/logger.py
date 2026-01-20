import json
from datetime import datetime

LOG_FILE = "backend/logs.jsonl"

def log_event(event_type, data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "data": data
        }) + "\n")
