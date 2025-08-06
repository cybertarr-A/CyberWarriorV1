# cyberwarrior_core/utils/mappings.py

vulnerability_labels = {
    0: "XSS",
    1: "RCE",
    2: "SQL Injection",
    3: "IDOR",
    4: "CSRF",
    5: "Directory Traversal",
    6: "Buffer Overflow",
    # add more if your model supports them
}

def get_label(class_id):
    return vulnerability_labels.get(class_id, "Unknown")
