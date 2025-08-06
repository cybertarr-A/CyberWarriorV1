# modules/classifier.py
import torch

labels = ["Low", "Medium", "High", "Critical"]

def classify_vulnerability(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return labels[predicted_class]

def classify_vulnerability_batch(texts, model, tokenizer):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_classes = torch.argmax(outputs.logits, dim=1).tolist()
    return [labels[i] for i in predicted_classes]
