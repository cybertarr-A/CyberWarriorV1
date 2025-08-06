# utils/data_processor.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from config import paths
from utils.logger import log

def load_raw_dataset(filename):
    path = os.path.join(paths["raw_data"], filename)
    if not os.path.exists(path):
        log.error(f"Raw dataset not found: {path}")
        return None
    try:
        df = pd.read_csv(path) if filename.endswith(".csv") else pd.read_json(path)
        log.info(f"Loaded raw dataset: {filename} with {len(df)} records.")
        return df
    except Exception as e:
        log.exception(f"Error loading dataset {filename}: {e}")
        return None

def clean_dataset(df):
    # Example: Drop rows with missing critical fields
    cleaned_df = df.dropna(subset=["description", "severity", "vulnerability_type"])
    log.info(f"Cleaned dataset: {len(cleaned_df)} rows remaining.")
    return cleaned_df

def preprocess_dataset(df):
    # Optional preprocessing: label encoding, vectorization, etc.
    df["severity_level"] = df["severity"].map({"low": 0, "medium": 1, "high": 2, "critical": 3})
    df = df.dropna(subset=["severity_level"])
    log.info("Preprocessed dataset for model input.")
    return df

def save_processed_dataset(df, filename="processed_vulns.csv"):
    path = os.path.join(paths["processed_data"], filename)
    os.makedirs(paths["processed_data"], exist_ok=True)
    df.to_csv(path, index=False)
    log.info(f"Saved processed dataset to {path}")

def split_dataset(df, test_size=0.2):
    train, test = train_test_split(df, test_size=test_size, random_state=42)
    log.info(f"Split dataset into train ({len(train)}) and test ({len(test)})")
    return train, test
