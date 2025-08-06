# modules/ai_engine.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from urllib.parse import urlparse
import os

# === Configuration ===
LABELS = ["Low", "Medium", "High", "Critical"]
MODEL_PATH = r"C:\CyberWarriorV1\models\cyberwarrior-core"

# === Load Model & Tokenizer ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.eval()

# === AI Core Functions ===
def run_ai(target):
    print(f"\n[🤖 AI Engine] Running AI analysis on: {target}")
    parsed = urlparse(target)
    text_input = f"Analyze domain {parsed.netloc}"
    result = classify(text_input)
    print(f"    ⬩ Overall Threat Rating: {result}")
    return result

def classify(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return LABELS[predicted_class]

def analyze_headers(headers):
    print("[🤖 AI Engine] Analyzing HTTP Headers")
    joined = " ".join([f"{k}: {v}" for k, v in headers.items()])
    return classify(joined)

def analyze_tech_stack(info):
    print("[🤖 AI Engine] Analyzing Technology Stack")
    if not info:
        return "Unknown"
    tech_text = " ".join(info) if isinstance(info, list) else str(info)
    return classify(tech_text)

def analyze_ports(open_ports):
    print("[🤖 AI Engine] Analyzing Open Ports")
    ports_text = "Open ports: " + ", ".join(map(str, open_ports))
    return classify(ports_text)
