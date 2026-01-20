import json

DB_FILE = "backend/analyses.json"

def save_analysis(analysis):
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(analysis)

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
