import joblib
import numpy as np
import pandas as pd
import os

# --------------------------------------------------------
# LOAD SCALER
# --------------------------------------------------------
SCALER_PATH = "models/audio_scaler.pkl"
scaler = joblib.load(SCALER_PATH)

# --------------------------------------------------------
# TRAITS AND MODELS
# --------------------------------------------------------
TRAITS = ["Overall", "Engaged", "Excited", "Calm", "Friendly", "Authentic", "NotStressed"]

MODEL_PATHS = {
    trait: f"models/model_xgbcv_{trait}.pkl"
    for trait in TRAITS
}

# Load all models at startup only once
models = {trait: joblib.load(path) for trait, path in MODEL_PATHS.items()}


# --------------------------------------------------------
# MAIN PREDICTION FUNCTION
# --------------------------------------------------------
def predict_traits_from_prosody(prosody_series):
    """
    prosody_series = pandas.Series from your extractor
    Returns dict of: {trait: score}
    """

    # Convert to DataFrame (model expects 2D)
    df = prosody_series.to_frame().T

    # DROP any extra columns not used during training
    training_feature_list = scaler.feature_names_in_  # these are the exact features used in training
    df = df.reindex(columns=training_feature_list)

    # scale
    X_scaled = scaler.transform(df)

    predictions = {}
    for trait in TRAITS:
        model = models[trait]
        pred = model.predict(X_scaled)[0]
        predictions[trait] = float(pred)

    return predictions
