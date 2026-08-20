import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def create_features_and_targets(df: pd.DataFrame, forecast_days: int = 5) -> pd.DataFrame:

    if df.empty:
        return df

    data = df.copy()

    data["Feat_Return"] = data["Close"].pct_change()

    if "RSI" in data.columns:
        data["Feat_RSI"] = data["RSI"] / 100.0

    if "ATR" in data.columns:
        data["Feat_ATR_Ratio"] = data["ATR"] / data["Close"]

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


def train_and_predict(df: pd.DataFrame, forecast_days: int = 5, train_window: int = 200) -> pd.DataFrame:
    processed_df = create_features_and_targets(df, forecast_days=forecast_days)

    if processed_df.empty:
        print("[Sentinel] Predictor error: Insufficient data to train the model.")
        return df

    feature_cols = [col for col in processed_df.columns if col.startswith("Feat_")]

    trainable_df = processed_df.dropna(subset=["Target_Direction"]).copy()

    if len(trainable_df) < train_window + 10:
        print(
            f"[Sentinel] Predictor warning: Too few rows ({len(trainable_df)}) for rolling window size ({train_window}).")
        return df

    probabilities = [np.nan] * len(processed_df)

    for i in range(train_window, len(trainable_df)):
        train_chunk = trainable_df.iloc[i - train_window: i]

        X_train = train_chunk[feature_cols]
        y_train = train_chunk["Target_Direction"].astype(int)

        model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X_train, y_train)

        X_test = trainable_df.iloc[[i]][feature_cols]
        probabilities[i] = model.predict_proba(X_test)[0, 1]

    processed_df["AI_Probability"] = probabilities
    processed_df["AI_Probability"] = processed_df["AI_Probability"].fillna(0.50)

    processed_df["AI_Signal"] = (processed_df["AI_Probability"] > 0.55).astype(int)

    print(f"[Sentinel] Rolling Walk-Forward completed (Window size: {train_window}). Features: {feature_cols}")
    return processed_df