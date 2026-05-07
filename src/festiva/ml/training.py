"""
Budget Prediction Engine - Training Pipeline
Generates synthetic dataset and trains RandomForest models for Bengaluru event budget prediction.
"""

import pickle
import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.preprocessing import StandardScaler

from festiva.config import MODELS_DIR, RANDOM_SEED, N_EVENTS

warnings.filterwarnings("ignore")
np.random.seed(RANDOM_SEED)

# Market rate splits by event type (percentages)
MARKET_SPLITS = {
    "Wedding": {"catering": 0.50, "venue": 0.30, "decor": 0.20},
    "Corporate": {"catering": 0.35, "venue": 0.40, "decor": 0.25},
    "Birthday": {"catering": 0.45, "venue": 0.30, "decor": 0.25},
}


def generate_synthetic_data(n_events: int = N_EVENTS) -> pd.DataFrame:
    """Generate synthetic event dataset for Bengaluru 2026."""
    event_types = np.random.choice(
        ["Wedding", "Corporate", "Birthday"],
        size=n_events,
        p=[0.40, 0.35, 0.25],
    )
    guest_count = np.random.randint(100, 1201, size=n_events)
    total_budget = np.random.uniform(500000, 6000000, size=n_events)

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 12, 31)
    date_range = (end_date - start_date).days
    event_dates = [
        start_date + timedelta(days=int(x))
        for x in np.random.uniform(0, date_range, n_events)
    ]
    event_month = np.array([d.month for d in event_dates])
    is_weekend = np.array([1 if d.weekday() >= 5 else 0 for d in event_dates])

    catering_spend = np.zeros(n_events)
    venue_spend = np.zeros(n_events)
    decor_spend = np.zeros(n_events)

    for i, event_type in enumerate(event_types):
        splits = MARKET_SPLITS[event_type]
        variance = np.random.uniform(0.95, 1.05)

        catering_spend[i] = total_budget[i] * splits["catering"] * variance
        venue_spend[i] = total_budget[i] * splits["venue"] * variance
        decor_spend[i] = total_budget[i] * splits["decor"] * variance

        total_allocated = catering_spend[i] + venue_spend[i] + decor_spend[i]
        if total_allocated > 0:
            catering_spend[i] = (catering_spend[i] / total_allocated) * total_budget[i]
            venue_spend[i] = (venue_spend[i] / total_allocated) * total_budget[i]
            decor_spend[i] = (decor_spend[i] / total_allocated) * total_budget[i]

    return pd.DataFrame(
        {
            "event_type": event_types,
            "guest_count": guest_count,
            "total_budget": total_budget,
            "event_month": event_month,
            "is_weekend": is_weekend,
            "catering_spend": catering_spend,
            "venue_spend": venue_spend,
            "decor_spend": decor_spend,
        }
    )


def train_models(df: pd.DataFrame) -> dict:
    """Train RandomForest models for budget prediction."""
    event_type_encoded = pd.get_dummies(df["event_type"], prefix="event_type")
    df_features = pd.concat(
        [df[["guest_count", "total_budget", "event_month", "is_weekend"]], event_type_encoded],
        axis=1,
    )

    X = df_features.values
    y_catering = df["catering_spend"].values
    y_venue = df["venue_spend"].values
    y_decor = df["decor_spend"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_cat_train, y_cat_test = train_test_split(
        X_scaled, y_catering, test_size=0.2, random_state=RANDOM_SEED
    )
    _, _, y_ven_train, y_ven_test = train_test_split(
        X_scaled, y_venue, test_size=0.2, random_state=RANDOM_SEED
    )
    _, _, y_dec_train, y_dec_test = train_test_split(
        X_scaled, y_decor, test_size=0.2, random_state=RANDOM_SEED
    )

    rf_params = {
        "n_estimators": 100,
        "max_depth": 15,
        "min_samples_split": 5,
        "random_state": RANDOM_SEED,
        "n_jobs": -1,
    }

    catering_model = RandomForestRegressor(**rf_params)
    catering_model.fit(X_train, y_cat_train)

    venue_model = RandomForestRegressor(**rf_params)
    venue_model.fit(X_train, y_ven_train)

    decor_model = RandomForestRegressor(**rf_params)
    decor_model.fit(X_train, y_dec_train)

    # Evaluation
    metrics = {}
    for name, model, y_test in [
        ("catering", catering_model, y_cat_test),
        ("venue", venue_model, y_ven_test),
        ("decor", decor_model, y_dec_test),
    ]:
        y_pred = model.predict(X_test)
        metrics[name] = {
            "r2": r2_score(y_test, y_pred),
            "rmse": root_mean_squared_error(y_test, y_pred),
        }

    return {
        "catering_model": catering_model,
        "venue_model": venue_model,
        "decor_model": decor_model,
        "feature_scaler": scaler,
        "feature_names": list(df_features.columns),
        "metrics": metrics,
    }


def save_engine(engine: dict, path=None):
    """Save trained models to disk."""
    if path is None:
        path = MODELS_DIR / "budget_engine.pkl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(engine, f)
    print(f"Budget engine saved to {path}")


def main():
    """Run the full training pipeline."""
    print("=" * 70)
    print("FESTIVA - BUDGET PREDICTION ENGINE TRAINING")
    print("=" * 70)

    print("\n[1/3] Generating synthetic dataset...")
    df = generate_synthetic_data()
    print(f"      Generated {len(df)} events")

    print("\n[2/3] Training RandomForest models...")
    engine = train_models(df)
    for name, m in engine["metrics"].items():
        print(f"      {name}: R²={m['r2']:.4f}, RMSE=₹{m['rmse']:,.0f}")

    print("\n[3/3] Saving budget engine...")
    save_engine(engine)
    print("\nTraining complete.")


if __name__ == "__main__":
    main()
