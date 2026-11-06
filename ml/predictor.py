import joblib
from pathlib import Path
import pandas as pd
import math
import json


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / 'models'
    / 'random_forest_fd001.joblib'
)
METADATA_PATH = (
    Path(__file__).resolve().parent.parent
    / 'models'
    / 'model_metadata.json'
)


def load_metadata():
    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_PATH}"
        )

    with open(METADATA_PATH, 'r') as file:
        metadata = json.load(file)

    return metadata

FEATURE_COLUMNS = load_metadata()['feature_schema']['features']

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    return model


def predict_rul(input_data):
    if not isinstance(input_data, dict):
        raise TypeError("Input data must be a dictionary.")

    missing_features = [
        feature for feature in FEATURE_COLUMNS
        if feature not in input_data
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    try:
        numeric_values = [
            float(input_data[feature])
            for feature in FEATURE_COLUMNS
        ]
    except (TypeError, ValueError):
        raise ValueError(
            "All feature values must be numeric."
        ) from None

    if not all(math.isfinite(value) for value in numeric_values):
        raise ValueError(
            "All feature values must be finite numbers."
        )

    input_df = pd.DataFrame(
        [numeric_values],
        columns=FEATURE_COLUMNS
    )

    model = load_model()
    prediction = model.predict(input_df)

    return float(prediction[0])


def predict_batch(input_data_list):
    if not isinstance(input_data_list, list):
        raise TypeError("Input data must be a list.")

    if not input_data_list:
        raise ValueError("Input data list cannot be empty.")

    input_rows = []

    for input_data in input_data_list:

        if not isinstance(input_data, dict):
            raise TypeError("Each observation must be a dictionary.")

        missing_features = [
            feature for feature in FEATURE_COLUMNS
            if feature not in input_data
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}"
            )

        try:
            numeric_values = [
                float(input_data[feature])
                for feature in FEATURE_COLUMNS
            ]
        except (TypeError, ValueError):
            raise ValueError(
                "All feature values must be numeric."
            ) from None

        if not all(math.isfinite(value) for value in numeric_values):
            raise ValueError(
                "All feature values must be finite numbers."
            )

        input_rows.append(numeric_values)

    input_df = pd.DataFrame(
        input_rows,
        columns=FEATURE_COLUMNS
    )

    model = load_model()
    predictions = model.predict(input_df)

    return predictions.tolist()