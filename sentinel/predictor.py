import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def create_features_and_targets(df: pd.DataFrame, forecast_days: int = 5) -> pd.DataFrame:
    """
    Generates machine learning features from price and technical indicators,
    and sets the target variable for directional prediction without dropping recent data.
    """
    if df.empty:
        return df

    data = df.copy()

    data["Feat_Return"] = data["Close"].pct_change()

    if "RSI" in data.columns:
        data["Feat_RSI"] = data["RSI"] / 100.0

    sma_cols = [col for col in data.columns if col.startswith("SMA_")]
    if len(sma_cols) >= 2:
        sorted_smas = sorted(sma_cols, key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 0)
        data["Feat_SMA_Ratio"] = data[sorted_smas[0]] / data[sorted_smas[-1]]
    else:
        data["Feat_SMA_Ratio"] = data["Close"].rolling(20).mean() / data["Close"].rolling(50).mean()

    data["Target_Direction"] = (
            data["Close"].shift(-forecast_days) > data["Close"]
    ).astype("Int64")

    feature_cols = [col for col in data.columns if col.startswith("Feat_")]
    cleaned_data = data.dropna(subset=feature_cols).copy()

    print(f"[Sentinel] Predictor dataset ready. Total usable rows for prediction: {len(cleaned_data)}")
    return cleaned_data


def train_and_predict(df: pd.DataFrame, forecast_days: int = 5) -> pd.DataFrame:
    """
    Trains a RandomForest model using an 80/20 chronological Train/Test split
    and appends 'AI_Signal' and 'AI_Probability' columns to the dataframe.
    """
    processed_df = create_features_and_targets(df, forecast_days=forecast_days)

    if processed_df.empty:
        print("[Sentinel] Predictor error: Insufficient data to train the model.")
        return df

    feature_cols = [col for col in processed_df.columns if col.startswith("Feat_")]

    trainable_df = processed_df.dropna(subset=["Target_Direction"]).copy()

    if len(trainable_df) < 30:
        print("[Sentinel] Predictor warning: Too few rows for reliable training.")
        return df

    split_idx = int(len(trainable_df) * 0.8)

    train_data = trainable_df.iloc[:split_idx]

    X_train = train_data[feature_cols]
    y_train = train_data["Target_Direction"].astype(int)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    X_all = processed_df[feature_cols]

    processed_df["AI_Probability"] = model.predict_proba(X_all)[:, 1]
    processed_df["AI_Signal"] = (processed_df["AI_Probability"] > 0.55).astype(int)

    print(
        f"[Sentinel] Predictor model successfully trained (Train size: {len(X_train)}). Features used: {feature_cols}")
    return processed_df
