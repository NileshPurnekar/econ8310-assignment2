# -*- coding: utf-8 -*-
"""assignment2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1In-Eh6M-rjpm9jSrhvO-JVR1_xmq5K9K
"""

import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- Function Definitions ---

def load_and_prepare_training_data(url):
    df = pd.read_csv(url)
    labels = df["meal"]
    features = df.drop(columns=["meal", "id", "DateTime"], errors="ignore")
    features = pd.get_dummies(features, drop_first=True)
    return features, labels

def load_and_prepare_test_data(url, reference_columns):
    test_df = pd.read_csv(url)
    test_features = test_df.drop(columns=["id", "DateTime"], errors="ignore")
    test_features = pd.get_dummies(test_features, drop_first=True)
    test_features = test_features.reindex(columns=reference_columns, fill_value=0)
    return test_features

def train_model(X_train, y_train):
    model = XGBClassifier(
        n_estimators=100,
        max_depth=8,
        learning_rate=0.2,
        objective="binary:logistic",
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def convert_predictions(pred_array):
    return [int(p.item()) if hasattr(p, 'item') else int(p) for p in pred_array]

# --- Main Workflow ---

def main():
    # URLs
    train_data_url = "https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/assignment3.csv"
    test_data_url = "https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/assignment3test.csv"

    # Load and split training data
    X, y = load_and_prepare_training_data(train_data_url)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and evaluate model
    model = train_model(X_train, y_train)
    val_preds = convert_predictions(model.predict(X_val))
    val_accuracy = accuracy_score(y_val, val_preds)
    print(f"Validation Accuracy: {val_accuracy:.2f}")

    # Retrain on full dataset
    final_model = train_model(X, y)
    joblib.dump(final_model, "modelFit.pkl")

    # Prepare test data and make predictions
    X_test = load_and_prepare_test_data(test_data_url, X.columns)
    test_preds = convert_predictions(final_model.predict(X_test))

    # Debug info (optional)
    print("Number of predictions:", len(test_preds))
    print("First 5 predictions:", test_preds[:5])
    print("Prediction data types:", set(type(p) for p in test_preds))

    # Save predictions to CSV
    output_df = pd.DataFrame(test_preds, columns=["meal_prediction"])
    output_df.to_csv("predictions.csv", index=False)

    # Final message
    print("Model training and prediction completed successfully.")

# Run main only if script is executed directly
if __name__ == "__main__":
    main()