# modules/memory.py

memory_log = {}

def remember_finding(target, message):
    if target not in memory_log:
        memory_log[target] = []
    memory_log[target].append(message)
    print(f"[Memory] {target}: {message}")

def list_memory():
    for target, messages in memory_log.items():
        print(f"Memory log for {target}:")
        for msg in messages:
            print(f"  - {msg}")
