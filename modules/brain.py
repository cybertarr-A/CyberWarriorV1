# modules/brain.py

import json
import os

MEMORY_FILE = os.path.join("brain", "memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def remember_finding(target, finding):
    memory = load_memory()
    if target not in memory:
        memory[target] = []
    if finding not in memory[target]:
        memory[target].append(finding)
        print(f"🧠 Brain memorized: {finding}")
    save_memory(memory)

def list_memory():
    memory = load_memory()
    print("\n🧠 Memory Log")
    for target, findings in memory.items():
        print(f"→ {target}")
        for f in findings:
            print(f"   - {f}")
