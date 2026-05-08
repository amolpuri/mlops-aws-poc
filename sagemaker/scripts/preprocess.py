"""
SageMaker Processing Script
----------------------------
Reads raw data from /opt/ml/processing/input,
cleans & transforms it, trains a simple model,
and writes predictions to /opt/ml/processing/output.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
import joblib

INPUT_PATH = "/opt/ml/processing/input"
OUTPUT_PATH = "/opt/ml/processing/output"


def load_data():
    files = [f for f in os.listdir(INPUT_PATH) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError(f"No CSV files found in {INPUT_PATH}")
    df = pd.concat([pd.read_csv(os.path.join(INPUT_PATH, f)) for f in files])
    print(f"Loaded {len(df)} rows from {len(files)} file(s).")
    return df


def preprocess(df: pd.DataFrame):
    # Drop rows with missing values
    df = df.dropna()

    # Separate features and label (adjust column names to your dataset)
    target_col = df.columns[-1]
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Encode categorical columns
    X = pd.get_dummies(X)

    return train_test_split(X, y, test_size=0.2, random_state=42)


def train(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_val, y_val):
    preds = model.predict(X_val)
    acc = accuracy_score(y_val, preds)
    prec = precision_score(y_val, preds, average="weighted", zero_division=0)
    print(f"Validation Accuracy : {acc:.4f}")
    print(f"Validation Precision: {prec:.4f}")
    return preds


def save_outputs(model, X_val, preds):
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Save model
    model_path = os.path.join(OUTPUT_PATH, "model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    # Save predictions
    results = X_val.copy()
    results["prediction"] = preds
    output_csv = os.path.join(OUTPUT_PATH, "predictions.csv")
    results.to_csv(output_csv, index=False)
    print(f"Predictions saved to {output_csv}")


if __name__ == "__main__":
    df = load_data()
    X_train, X_val, y_train, y_val = preprocess(df)
    model = train(X_train, y_train)
    preds = evaluate(model, X_val, y_val)
    save_outputs(model, X_val, preds)
