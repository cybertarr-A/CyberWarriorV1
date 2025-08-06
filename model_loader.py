# cyberwarrior_core/model_loader.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def load_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    return tokenizer, model, device
