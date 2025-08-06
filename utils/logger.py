import logging
import os
import sys
from config import paths

def setup_logger(name="CyberWarrior"):
    try:
        # Try using configured path
        log_path = paths.get("log_file", "logs/cyberwarrior.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
    except Exception as e:
        # Fallback to home directory
        fallback_log_path = os.path.join(os.path.expanduser("~"), "cyberwarrior.log")
        print(f"[Logger Warning] Failed to write to configured log path. Using fallback: {fallback_log_path}")
        try:
            file_handler = logging.FileHandler(fallback_log_path, encoding='utf-8')
        except Exception as e2:
            raise RuntimeError(f"[Logger Error] Cannot write to fallback log file: {e2}")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    # Set handlers
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

# Instantiate the global logger
log = setup_logger()
