# config.py
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config", "config.json")

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"[CONFIG] Missing config file at {CONFIG_FILE}")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

# Access settings like this
paths = {
    "project_name": config.get("project_name"),
    "raw_data": config.get("raw_data"),
    "processed_data": config.get("processed_data"),
    "result_dir": config.get("result_dir"),
    "models": config.get("models"),
    "log_file": config.get("log_file", os.path.join("logs", "cyberwarrior.log")),
    "memory": config.get("memory"),
    "tokenizer_dir": config.get("tokenizer_dir"),
    "model_dir": config.get("model_dir"),
    "ai_analysis_results": config.get("ai_analysis_results")
}

# Make sure all paths exist
for key, path in paths.items():
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


