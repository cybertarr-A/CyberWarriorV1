import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from utils.logger import log
from utils.data_processor import (
    load_raw_dataset,
    clean_dataset,
    preprocess_dataset,
    save_processed_dataset,
)
from config import paths

MODEL_PATH = r"C:\CyberWarriorV1\models\cyberwarrior-core"
LABELS = ["Low", "Medium", "High", "Critical"]


class AICoreModel:
    def __init__(self):
        print("Loading transformer model for AI classification...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
        self.model.eval()
        print("Transformer model loaded.")

    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
        return LABELS[predicted_class]

    def classify_batch(self, texts):
        inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        predicted_classes = torch.argmax(outputs.logits, dim=1).tolist()
        return [LABELS[i] for i in predicted_classes]

    def analyze(self, input_file):
        log.info(f"Starting AI analysis for file: {input_file}")

        df = load_raw_dataset(input_file)
        if df is None:
            log.error("Failed to load dataset.")
            return []

        df_clean = clean_dataset(df)
        df_processed = preprocess_dataset(df_clean)
        save_processed_dataset(df_processed)

        if "description" not in df_processed.columns:
            log.error("Missing 'description' column for text classification.")
            return []

        df_processed["predicted_severity"] = self.classify_batch(
            df_processed["description"].tolist()
        )
        log.info("Transformer-based AI classification complete.")

        result_path = os.path.join(paths["processed_data"], "ai_analysis_results.csv")
        df_processed.to_csv(result_path, index=False)
        log.info(f"Saved AI analysis results to: {result_path}")

        return df_processed["predicted_severity"].tolist()


class AICore:
    def __init__(self):
        print("AICore initialized")

    def analyze(self, recon_data, scan_data, exploit_data):
        summary = []

        if recon_data:
            summary.append(f"Recon headers found: {len(getattr(recon_data, 'headers', {}))}")
        if scan_data:
            summary.append(f"Open ports found: {len(getattr(scan_data, 'open_ports', []))}")
        if exploit_data:
            summary.append(f"Exploit findings count: {len(getattr(exploit_data, 'findings', []))}")

        if not summary:
            return "No data available for AI analysis."

        return "\n".join(summary)
