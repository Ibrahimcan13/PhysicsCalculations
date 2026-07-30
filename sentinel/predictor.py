import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def create_features_and_targets(df: pd.DataFrame, forecast_days: int = 5) -> pd.DataFrame:
    """
    Generates machine learning features from price and technical indicators,
    and sets the target variable for directional prediction.
    """
    if df.empty:
        return df

    data = df.copy()

    data["Feat_Return"] = data["Close"].pct_change()

    if "RSI" in data.columns:
        data["Feat_RSI"] = data["RSI"] / 100.0

    if "SMA_50" in data.columns and "SMA_200" in data.columns:
        data["Feat_SMA_Ratio"] = data["SMA_50"] / data["SMA_200"]

    data["Target_Direction"] = (
            data["Close"].shift(-forecast_days) > data["Close"]
    ).astype(int)

    cleaned_data = data.dropna().copy()

    print(f"[Sentinel] Predictor dataset ready. Target horizon: {forecast_days} days. Usable rows: {len(cleaned_data)}")
    return cleaned_data


def train_and_predict(df: pd.DataFrame, forecast_days: int = 5) -> pd.DataFrame:
    """
    Trains a RandomForest model on extracted features and appends
    'AI_Signal' and 'AI_Probability' columns to the dataframe.
    """
    processed_df = create_features_and_targets(df, forecast_days=forecast_days)

    if processed_df.empty:
        print("[Sentinel] Predictor error: Insufficient data to train the model.")
        return df

    feature_cols = [col for col in processed_df.columns if col.startswith("Feat_")]
    X = processed_df[feature_cols]
    y = processed_df["Target_Direction"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    processed_df["AI_Probability"] = model.predict_proba(X)[:, 1]

    processed_df["AI_Signal"] = (processed_df["AI_Probability"] > 0.55).astype(int)

    print(f"[Sentinel] Predictor model successfully trained. Features used: {feature_cols}")
    return processed_df