import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


def create_features_and_targets(df: pd.DataFrame, forecast_days: int = 5) -> pd.DataFrame:
    if df.empty:
        return df

    data = df.copy()

    data["Feat_Return"] = data["Close"].pct_change().fillna(0.0)

    if "RSI" in data.columns:
        data["Feat_RSI"] = (data["RSI"] / 100.0).fillna(0.50)
    else:
        data["Feat_RSI"] = 0.50

    if "ATR" in data.columns:
        data["Feat_ATR_Ratio"] = (data["ATR"] / (data["Close"] + 1e-9)).fillna(0.0)
    else:
        data["Feat_ATR_Ratio"] = 0.0

    if "Kalman" in data.columns:
        data["Feat_Kalman_Ratio"] = (data["Close"] / (data["Kalman"] + 1e-9)).fillna(1.0)
    else:
        data["Feat_Kalman_Ratio"] = 1.0

    sma_cols = [col for col in data.columns if col.startswith("SMA_")]
    if len(sma_cols) >= 2:
        sorted_smas = sorted(sma_cols, key=lambda x: int(x.split("_")[1]) if x.split("_")[1].isdigit() else 0)
        data["Feat_SMA_Ratio"] = (data[sorted_smas[0]] / (data[sorted_smas[-1]] + 1e-9)).fillna(1.0)
    else:
        sma_20 = data["Close"].rolling(20).mean()
        sma_50 = data["Close"].rolling(50).mean()
        data["Feat_SMA_Ratio"] = (sma_20 / (sma_50 + 1e-9)).fillna(1.0)

    target_series = (data["Close"].shift(-forecast_days) > data["Close"]).astype(float)
    data["Target_Direction"] = target_series.fillna(0.0).astype(int)

    return data


def train_and_predict(
    df: pd.DataFrame,
    forecast_days: int = 5,
    train_window: int = 200,
    retrain_step: int = 20
) -> pd.DataFrame:
    processed_df = create_features_and_targets(df, forecast_days=forecast_days)

    if processed_df.empty:
        print("[Sentinel] Predictor error: Insufficient data to train the model.")
        return df

    feature_cols = [col for col in processed_df.columns if col.startswith("Feat_")]

    if len(processed_df) < train_window + forecast_days + 10:
        print(f"[Sentinel] Predictor warning: Too few rows ({len(processed_df)}) for rolling window size ({train_window}).")
        return df

    probabilities = [0.50] * len(processed_df)
    current_model = None
    scaler = None

    for i in range(train_window + forecast_days, len(processed_df)):
        if (i - (train_window + forecast_days)) % retrain_step == 0 or current_model is None:
            train_end_idx = i - forecast_days
            train_start_idx = train_end_idx - train_window

            train_chunk = processed_df.iloc[train_start_idx:train_end_idx]
            X_train = train_chunk[feature_cols]
            y_train = train_chunk["Target_Direction"]

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)

            current_model = RandomForestClassifier(
                n_estimators=50,
                max_depth=5,
                min_samples_leaf=5,
                class_weight="balanced",
                n_jobs=-1,
                random_state=42
            )
            current_model.fit(X_train_scaled, y_train)

        X_test = processed_df.iloc[[i]][feature_cols]
        X_test_scaled = scaler.transform(X_test)
        probabilities[i] = current_model.predict_proba(X_test_scaled)[0, 1]

    processed_df["AI_Probability"] = probabilities
    processed_df["AI_Signal"] = (processed_df["AI_Probability"] > 0.55).astype(np.int8)

    print(
        f"[Sentinel] Purged Walk-Forward completed with Imputed Features (Gap: {forecast_days}d, n_jobs=-1 Active) "
        f"(Window: {train_window}, Retrain Step: {retrain_step}d). "
        f"Features: {feature_cols}"
    )
    return processed_df