"""Train the scaler and nearest-neighbor index used by app1.py.

Run from this directory with: python train_artifacts.py
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


BASE = Path(__file__).resolve().parent
ARTIFACTS = BASE / "artifacts"
FEATURES_CSV = BASE / "fma_features_processed.csv"
FEATURE_COLUMNS_JSON = ARTIFACTS / "feature_cols.json"


def main():
    feature_cols = json.loads(FEATURE_COLUMNS_JSON.read_text(encoding="utf-8"))
    frame = pd.read_csv(FEATURES_CSV)
    missing = [col for col in feature_cols if col not in frame.columns]
    if missing:
        raise ValueError(f"Feature CSV is missing required columns: {missing}")

    matrix = frame[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0).to_numpy(dtype=np.float64)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(matrix)

    neighbors = NearestNeighbors(metric="euclidean", algorithm="auto")
    neighbors.fit(scaled)

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, ARTIFACTS / "scaler.joblib")
    joblib.dump(neighbors, ARTIFACTS / "nn.joblib")
    print(f"Saved model artifacts for {len(matrix)} tracks and {len(feature_cols)} features.")


if __name__ == "__main__":
    main()
