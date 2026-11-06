

import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ==========================================
# 1. Load prepared data
# ==========================================

X_train = pd.read_csv('data/processed/X_train.csv')
X_val = pd.read_csv('data/processed/X_val.csv')

y_train = pd.read_csv(
    'data/processed/y_train.csv'
).squeeze()

y_val = pd.read_csv(
    'data/processed/y_val.csv'
).squeeze()

print("Training features:", X_train.shape)
print("Training target:", y_train.shape)

print("Validation features:", X_val.shape)
print("Validation target:", y_val.shape)


# ==========================================
# 2. Create and train Random Forest model
# ==========================================

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

print("\nRandom Forest model trained successfully!")


# ==========================================
# 3. Predict validation data
# ==========================================

y_pred = model.predict(X_val)

print("\nFirst 10 predicted RUL values:")
print(y_pred[:10])


# ==========================================
# 4. Compare actual and predicted values
# ==========================================

comparison = pd.DataFrame({
    'Actual_RUL': y_val.iloc[:10].values,
    'Predicted_RUL': y_pred[:10]
})

print("\nActual vs Predicted RUL:")
print(comparison)


# ==========================================
# 5. Row-level evaluation
# ==========================================

mae = mean_absolute_error(y_val, y_pred)

rmse = mean_squared_error(
    y_val,
    y_pred
) ** 0.5

print("\nRow-level Model Evaluation:")
print("MAE:", mae)
print("RMSE:", rmse)


# ==========================================
# 6. Load validation metadata
# ==========================================

val_metadata = pd.read_csv(
    'data/processed/val_metadata.csv'
)

print("\nValidation metadata:")
print(val_metadata.head())

print(
    "\nNumber of validation engines:",
    val_metadata['engine_id'].nunique()
)


# ==========================================
# 7. Attach predictions to metadata
# ==========================================

val_results = val_metadata.copy()

val_results['predicted_RUL'] = y_pred


# Find each engine's complete lifetime

val_results['max_cycle'] = (
    val_results.groupby('engine_id')['cycle']
    .transform('max')
)


# ==========================================
# 8. Multi-point validation
# ==========================================

observation_points = [0.50, 0.60, 0.70, 0.80]

simulated_results = []

for percentage in observation_points:

    # Calculate selected observation cycle

    val_results['cutoff_cycle'] = (
        val_results['max_cycle'] * percentage
    ).astype(int)

    selected = val_results[
        val_results['cycle'] == val_results['cutoff_cycle']
    ].copy()

    selected['observation_percentage'] = percentage * 100

    simulated_results.append(selected)


# Combine all observation points

multi_point_results = pd.concat(
    simulated_results,
    ignore_index=True
)


print("\nMulti-point validation results:")

print(
    multi_point_results[
        [
            'engine_id',
            'observation_percentage',
            'cycle',
            'RUL',
            'predicted_RUL'
        ]
    ].sort_values(
        ['engine_id', 'observation_percentage']
    ).to_string(index=False)
)


# ==========================================
# 9. Evaluation by observation point
# ==========================================

print("\nEvaluation by observation point:")

for percentage in observation_points:

    point_data = multi_point_results[
        multi_point_results['observation_percentage']
        == percentage * 100
    ]

    point_mae = mean_absolute_error(
        point_data['RUL'],
        point_data['predicted_RUL']
    )

    point_rmse = mean_squared_error(
        point_data['RUL'],
        point_data['predicted_RUL']
    ) ** 0.5

    print(
        f"{percentage * 100:.0f}% lifetime | "
        f"Engines: {len(point_data)} | "
        f"MAE: {point_mae:.2f} | "
        f"RMSE: {point_rmse:.2f}"
    )


# ==========================================
# 10. Prediction error analysis
# ==========================================

multi_point_results['error'] = (
    multi_point_results['predicted_RUL']
    - multi_point_results['RUL']
)

overestimated = multi_point_results[
    multi_point_results['error'] > 0
]

underestimated = multi_point_results[
    multi_point_results['error'] < 0
]

print("\nPrediction error summary:")

print("Total observations:", len(multi_point_results))

print("Overestimated observations:", len(overestimated))

print("Underestimated observations:", len(underestimated))

print(
    "Exact predictions:",
    (multi_point_results['error'] == 0).sum()
)

print(
    "Average overestimation:",
    overestimated['error'].mean()
)

print(
    "Average underestimation:",
    underestimated['error'].mean()
)


# ==========================================
# Official NASA test dataset preparation
# ==========================================

columns = (
    ['engine_id', 'cycle']
    + [f'op_setting_{i}' for i in range(1, 4)]
    + [f'sensor_{i}' for i in range(1, 22)]
)

test_df = pd.read_csv(
    'data/raw/test_FD001.txt',
    sep=r'\s+',
    header=None,
    names=columns
)

actual_rul = pd.read_csv(
    'data/raw/RUL_FD001.txt',
    sep=r'\s+',
    header=None,
    names=['actual_RUL']
)

# Select the final observation for each engine

test_last = (
    test_df.groupby('engine_id')
    .tail(1)
    .sort_values('engine_id')
    .reset_index(drop=True)
)

# Select exactly the same features used during training

X_test = test_last[X_train.columns]

y_test = actual_rul['actual_RUL']

print("\nOfficial test dataset:")
print("Test observations:", test_df.shape)
print("Test engines:", test_last['engine_id'].nunique())
print("Test features:", X_test.shape)
print("Actual RUL values:", y_test.shape)

print("\nFirst 5 test engine observations:")
print(test_last[['engine_id', 'cycle']].head())

print("\nFirst 5 actual RUL values:")
print(y_test.head())

# ==========================================
# Official NASA test-set prediction
# ==========================================

y_test_pred = model.predict(X_test)

test_results = pd.DataFrame({
    'engine_id': test_last['engine_id'],
    'actual_RUL': y_test,
    'predicted_RUL': y_test_pred
})

print("\nOfficial NASA test predictions:")
print(test_results.head(10))


# ==========================================
# Official NASA test-set evaluation
# ==========================================

test_mae = mean_absolute_error(
    y_test,
    y_test_pred
)

test_rmse = mean_squared_error(
    y_test,
    y_test_pred
) ** 0.5

print("\nOfficial NASA Test Evaluation:")
print("Number of test engines:", len(test_results))
print("MAE:", test_mae)
print("RMSE:", test_rmse)


# ==========================================
# Official test prediction error analysis
# ==========================================

test_results['error'] = (
    test_results['predicted_RUL']
    - test_results['actual_RUL']
)

overestimated = test_results[
    test_results['error'] > 0
]

underestimated = test_results[
    test_results['error'] < 0
]

print("\nOfficial Test Error Analysis:")

print("Overestimated engines:", len(overestimated))
print("Underestimated engines:", len(underestimated))

print(
    "Exact predictions:",
    (test_results['error'] == 0).sum()
)

print(
    "Average overestimation:",
    overestimated['error'].mean()
)

print(
    "Average underestimation:",
    underestimated['error'].mean()
)

# Save the trained model
model_dir = Path('models')
model_dir.mkdir(parents=True, exist_ok=True)

model_path = model_dir / 'random_forest_fd001.joblib'

joblib.dump(model, model_path)

print(f"\nModel saved successfully: {model_path}")