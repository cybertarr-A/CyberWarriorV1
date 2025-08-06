# cyberwarrior_core/ai_inference.py

from cyberwarrior_core.model_loader import load_model
import torch

class CyberwarriorAI:
    def __init__(self, model_path):
        self.tokenizer, self.model, self.device = load_model(model_path)
        self.model.eval()

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            prediction = torch.argmax(logits, dim=1).item()
        return prediction
