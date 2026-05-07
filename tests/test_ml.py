"""Tests for ML training module."""

import pandas as pd

from festiva.ml.training import generate_synthetic_data, train_models


def test_generate_synthetic_data():
    df = generate_synthetic_data(n_events=100)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    assert set(df.columns) == {
        "event_type", "guest_count", "total_budget",
        "event_month", "is_weekend",
        "catering_spend", "venue_spend", "decor_spend",
    }


def test_train_models():
    df = generate_synthetic_data(n_events=200)
    engine = train_models(df)
    assert "catering_model" in engine
    assert "venue_model" in engine
    assert "decor_model" in engine
    assert "feature_scaler" in engine
    for name in ["catering", "venue", "decor"]:
        assert engine["metrics"][name]["r2"] > 0.9
