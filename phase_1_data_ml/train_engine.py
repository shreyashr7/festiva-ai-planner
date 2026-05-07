"""
Train Budget Prediction Engine for Bengaluru Event Planning
Generates synthetic dataset and trains RandomForest models to predict spending allocation.
"""

import numpy as np
import pandas as pd
import pickle
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)

print("=" * 80)
print("BENGALURU EVENT BUDGET PREDICTION ENGINE - TRAINING PIPELINE")
print("=" * 80)

# ============================================================================
# PHASE 1: SYNTHETIC DATA GENERATION
# ============================================================================
print("\n[1] Generating synthetic dataset of 1,200 events for Bengaluru in 2026...")

n_events = 1200

# Event type distribution (realistic proportions for Bengaluru)
event_types = np.random.choice(
    ['Wedding', 'Corporate', 'Birthday'],
    size=n_events,
    p=[0.40, 0.35, 0.25]  # Weddings most common, then Corporate, then Birthday
)

# Guest count: 100-1200 (log-normal distribution for realism)
guest_count = np.random.randint(100, 1201, size=n_events)

# Total budget in INR: ₹5L to ₹60L
total_budget = np.random.uniform(500000, 6000000, size=n_events)

# Date in 2026 (for seasonality features)
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 12, 31)
date_range = (end_date - start_date).days

event_dates = [start_date + timedelta(days=int(x)) for x in np.random.uniform(0, date_range, n_events)]
event_month = np.array([d.month for d in event_dates])
is_weekend = np.array([1 if d.weekday() >= 5 else 0 for d in event_dates])

# ============================================================================
# PHASE 2: BENGALURU MARKET-RATE BUDGET SPLITS
# ============================================================================
print("[2] Applying Bengaluru market-rate budget allocations...")

# Market rate splits by event type (percentages)
market_splits = {
    'Wedding': {'catering': 0.50, 'venue': 0.30, 'decor': 0.20},
    'Corporate': {'catering': 0.35, 'venue': 0.40, 'decor': 0.25},
    'Birthday': {'catering': 0.45, 'venue': 0.30, 'decor': 0.25}
}

catering_spend = np.zeros(n_events)
venue_spend = np.zeros(n_events)
decor_spend = np.zeros(n_events)

for i, event_type in enumerate(event_types):
    splits = market_splits[event_type]
    
    # Add realistic variance (±5%) to simulate actual deviations from market norms
    variance = np.random.uniform(0.95, 1.05)
    
    catering_spend[i] = total_budget[i] * splits['catering'] * variance
    venue_spend[i] = total_budget[i] * splits['venue'] * variance
    decor_spend[i] = total_budget[i] * splits['decor'] * variance
    
    # Normalize to ensure total equals budget (redistribute variance)
    total_allocated = catering_spend[i] + venue_spend[i] + decor_spend[i]
    if total_allocated > 0:
        catering_spend[i] = (catering_spend[i] / total_allocated) * total_budget[i]
        venue_spend[i] = (venue_spend[i] / total_allocated) * total_budget[i]
        decor_spend[i] = (decor_spend[i] / total_allocated) * total_budget[i]

# Create DataFrame
df = pd.DataFrame({
    'event_type': event_types,
    'guest_count': guest_count,
    'total_budget': total_budget,
    'event_month': event_month,
    'is_weekend': is_weekend,
    'catering_spend': catering_spend,
    'venue_spend': venue_spend,
    'decor_spend': decor_spend
})

print(f"   ✓ Generated {len(df)} events")
print(f"\n   Dataset Overview:")
print(df.head(10))
print(f"\n   Summary Statistics:")
print(df.describe().round(2))

# ============================================================================
# PHASE 3: FEATURE ENGINEERING
# ============================================================================
print("\n[3] Engineering features for model training...")

# One-hot encode event_type
event_type_encoded = pd.get_dummies(df['event_type'], prefix='event_type')
df_features = pd.concat([df[['guest_count', 'total_budget', 'event_month', 'is_weekend']], event_type_encoded], axis=1)

feature_names = list(df_features.columns)
print(f"   ✓ Features: {feature_names}")
print(f"   ✓ Feature matrix shape: {df_features.shape}")

# ============================================================================
# PHASE 4: MODEL TRAINING
# ============================================================================
print("\n[4] Training RandomForest models for spending predictions...")

# Prepare data
X = df_features.values
y_catering = df['catering_spend'].values
y_venue = df['venue_spend'].values
y_decor = df['decor_spend'].values

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_catering_train, y_catering_test = train_test_split(
    X_scaled, y_catering, test_size=0.2, random_state=42
)
_, _, y_venue_train, y_venue_test = train_test_split(
    X_scaled, y_venue, test_size=0.2, random_state=42
)
_, _, y_decor_train, y_decor_test = train_test_split(
    X_scaled, y_decor, test_size=0.2, random_state=42
)

# Train Catering Spend Model
print("   Training Catering Spend Model...")
catering_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
catering_model.fit(X_train, y_catering_train)
catering_pred = catering_model.predict(X_test)
catering_r2 = r2_score(y_catering_test, catering_pred)
catering_rmse = np.sqrt(mean_squared_error(y_catering_test, catering_pred))
print(f"      R² Score: {catering_r2:.4f}")
print(f"      RMSE: ₹{catering_rmse:,.2f}")

# Train Venue Spend Model
print("   Training Venue Spend Model...")
venue_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
venue_model.fit(X_train, y_venue_train)
venue_pred = venue_model.predict(X_test)
venue_r2 = r2_score(y_venue_test, venue_pred)
venue_rmse = np.sqrt(mean_squared_error(y_venue_test, venue_pred))
print(f"      R² Score: {venue_r2:.4f}")
print(f"      RMSE: ₹{venue_rmse:,.2f}")

# Train Decor Spend Model
print("   Training Decor Spend Model...")
decor_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
decor_model.fit(X_train, y_decor_train)
decor_pred = decor_model.predict(X_test)
decor_r2 = r2_score(y_decor_test, decor_pred)
decor_rmse = np.sqrt(mean_squared_error(y_decor_test, decor_pred))
print(f"      R² Score: {decor_r2:.4f}")
print(f"      RMSE: ₹{decor_rmse:,.2f}")

# ============================================================================
# PHASE 5: MODEL SERIALIZATION
# ============================================================================
print("\n[5] Serializing models and metadata...")

# Create metadata dictionary
metadata = {
    'training_date': datetime.now().isoformat(),
    'n_events': n_events,
    'feature_names': feature_names,
    'event_types': ['Wedding', 'Corporate', 'Birthday'],
    'training_metrics': {
        'catering_r2': float(catering_r2),
        'catering_rmse': float(catering_rmse),
        'venue_r2': float(venue_r2),
        'venue_rmse': float(venue_rmse),
        'decor_r2': float(decor_r2),
        'decor_rmse': float(decor_rmse),
        'test_set_size': len(X_test),
        'training_set_size': len(X_train)
    },
    'model_config': {
        'n_estimators': 100,
        'max_depth': 15,
        'min_samples_split': 5
    }
}

# Bundle everything into a single serializable object
budget_engine = {
    'catering_model': catering_model,
    'venue_model': venue_model,
    'decor_model': decor_model,
    'feature_scaler': scaler,
    'metadata': metadata,
    'version': '1.0'
}

# Save to pickle
output_path = 'budget_engine.pkl'
with open(output_path, 'wb') as f:
    pickle.dump(budget_engine, f)

print(f"   ✓ Models and scaler saved to: {output_path}")

# ============================================================================
# PHASE 6: VALIDATION & SUMMARY
# ============================================================================
print("\n[6] Validation & Summary...")

# Load and verify
with open(output_path, 'rb') as f:
    loaded_engine = pickle.load(f)

print(f"   ✓ Loaded budget_engine.pkl successfully")
print(f"   ✓ Contains: {list(loaded_engine.keys())}")
print(f"\n   Model Types:")
print(f"      - Catering Model: {type(loaded_engine['catering_model']).__name__}")
print(f"      - Venue Model: {type(loaded_engine['venue_model']).__name__}")
print(f"      - Decor Model: {type(loaded_engine['decor_model']).__name__}")
print(f"      - Feature Scaler: {type(loaded_engine['feature_scaler']).__name__}")

# Test inference on sample records
print(f"\n[7] Sample Predictions on 5 test records:")
print("-" * 80)

for i in range(min(5, len(X_test))):
    sample = X_test[i:i+1]
    pred_catering = loaded_engine['catering_model'].predict(sample)[0]
    pred_venue = loaded_engine['venue_model'].predict(sample)[0]
    pred_decor = loaded_engine['decor_model'].predict(sample)[0]
    pred_total = pred_catering + pred_venue + pred_decor
    actual_total = y_catering_test[i] + y_venue_test[i] + y_decor_test[i]
    error_pct = abs(pred_total - actual_total) / actual_total * 100
    
    print(f"   Sample {i+1}:")
    print(f"      Actual Total Budget:   ₹{actual_total:,.2f}")
    print(f"      Predicted Total:       ₹{pred_total:,.2f} (Error: {error_pct:.2f}%)")
    print(f"      Catering:  ₹{pred_catering:,.2f} | Venue: ₹{pred_venue:,.2f} | Decor: ₹{pred_decor:,.2f}")
    print()

print("=" * 80)
print("✓ TRAINING PIPELINE COMPLETE")
print(f"✓ Budget engine saved to: {output_path}")
print("=" * 80)
