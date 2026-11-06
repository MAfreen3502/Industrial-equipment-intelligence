import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

columns = (
    ['engine_id', 'cycle']
    + [f'op_setting_{i}' for i in range(1, 4)]
    + [f'sensor_{i}' for i in range(1, 22)]
)

train_df = pd.read_csv(
    'data/raw/train_FD001.txt',
    sep=r'\s+',
    header=None,
    names=columns
)

print("Training dataset shape:", train_df.shape)
print(train_df.head())

last_cycles = train_df.groupby('engine_id')['cycle'].max()

train_df['RUL'] = (
    train_df['engine_id'].map(last_cycles) - train_df['cycle']
)

print("\nTraining data with RUL:")
print(train_df[['engine_id', 'cycle', 'RUL']].head(10))

sensor_columns = [f'sensor_{i}' for i in range(1, 22)]

constant_sensors = [
    col for col in sensor_columns
    if train_df[col].nunique() == 1
]

print("\nConstant sensors:", constant_sensors)
print("Total constant sensors:", len(constant_sensors))

feature_columns = (
    [f'op_setting_{i}' for i in range(1, 4)]
    + [
        col for col in sensor_columns
        if col not in constant_sensors
    ]
)

X = train_df[feature_columns]
y = train_df['RUL']

print("\nFeature shape:", X.shape)
print("Target shape:", y.shape)
print("\nSelected features:")
print(feature_columns)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, val_idx = next(
    splitter.split(X, y, groups=train_df['engine_id'])
)

X_train = X.iloc[train_idx]
X_val = X.iloc[val_idx]

y_train = y.iloc[train_idx]
y_val = y.iloc[val_idx]

print("\nTraining features:", X_train.shape)
print("Validation features:", X_val.shape)

print("Training engines:", train_df.iloc[train_idx]['engine_id'].nunique())
print("Validation engines:", train_df.iloc[val_idx]['engine_id'].nunique())

print(
    "Common engines:",
    len(
        set(train_df.iloc[train_idx]['engine_id'])
        & set(train_df.iloc[val_idx]['engine_id'])
    )
)
print("\nFeature ranges:")
print(X_train.describe().loc[['min', 'max']].T)

X_train.to_csv('data/processed/X_train.csv', index=False)
X_val.to_csv('data/processed/X_val.csv', index=False)

y_train.to_csv('data/processed/y_train.csv', index=False)
y_val.to_csv('data/processed/y_val.csv', index=False)

print("\nPrepared datasets saved successfully!")
val_metadata = train_df.iloc[val_idx][
    ['engine_id', 'cycle', 'RUL']
].reset_index(drop=True)

val_metadata.to_csv(
    'data/processed/val_metadata.csv',
    index=False
)

print("\nValidation metadata saved successfully!")