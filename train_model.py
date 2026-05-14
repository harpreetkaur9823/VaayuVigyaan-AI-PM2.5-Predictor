"""
VaayuVigyaan AI — Model Training Script
Trains XGBoost PM2.5 predictor and saves to models/xgb_pm25_model.pkl
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data_generator import generate_training_data

try:
    from xgboost import XGBRegressor
    USE_XGB = True
except ImportError:
    from sklearn.ensemble import GradientBoostingRegressor
    USE_XGB = False
    print("XGBoost not found, using GradientBoosting fallback")


def train_and_save():
    print("🔄 Generating synthetic training data...")
    df = generate_training_data(n=8000)

    features = ["temperature", "humidity", "wind_speed", "rainfall",
                 "aod", "traffic_intensity", "industrial_activity"]
    X = df[features].values
    y = df["pm25"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    print("🤖 Training model...")
    if USE_XGB:
        model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        )
    else:
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42)

    model.fit(X_train_s, y_train)

    # Evaluate
    y_pred = model.predict(X_test_s)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f"✅ RMSE: {rmse:.2f} | R²: {r2:.3f}")

    # Feature importances
    importances = model.feature_importances_
    fi_df = pd.DataFrame({"feature": features, "importance": importances})
    fi_df = fi_df.sort_values("importance", ascending=False)
    print("\n📊 Feature Importances:")
    for _, row in fi_df.iterrows():
        bar = "█" * int(row.importance * 40)
        print(f"  {row.feature:25s} {bar} {row.importance:.3f}")

    # Save model + scaler
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/xgb_pm25_model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(features, "models/features.pkl")
    joblib.dump({"rmse": rmse, "r2": r2, "feature_importances": fi_df.to_dict()}, "models/metrics.pkl")

    print("\n💾 Model saved to models/xgb_pm25_model.pkl")
    return model, scaler, rmse, r2


if __name__ == "__main__":
    train_and_save()
