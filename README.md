# 🛡️ CyberWarriorV1

CyberWarrior is an AI-powered vulnerability scanning and penetration testing framework built with Python. It combines static analysis, dynamic scanning, transformer-based classification, memory logging, and automated reporting — built to assist bug bounty hunters and security researchers.

## 🚀 Features

- 🔍 **Recon & Scanning Module**
  - Port scanning (top 10)
  - HTTP header analysis
  - Tech stack fingerprinting
  - Endpoint discovery
  - SQL Injection (Error & Blind Time-based)

- 🧠 **AI Vulnerability Analysis**
  - Transformer-based classification using a custom `safetensors` model
  - Predicts severity (Low, Medium, High, Critical)
  - Supports batch classification from `.csv` or `.json` files

- 🧬 **Memory Engine**
  - Remembers past findings per target
  - Logs structured vulnerability memory in JSON format

- 📦 **Modular Architecture**
  - Easily extensible with plug-and-play modules (`scanner`, `exploit`, `report_generator`, etc.)
  - Centralized `core.py` for orchestration

- 📊 **Auto Report Generator**
  - Generates detailed output logs and saves analysis reports in CSV format

---
