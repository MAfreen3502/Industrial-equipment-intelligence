import pandas as pd

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

print(train_df.head())
print("\nDataset shape:", train_df.shape)

print("\nTotal engines:", train_df['engine_id'].nunique())

print("\nCycles per engine:")
print(train_df.groupby('engine_id')['cycle'].max().head(10))
print("\nMissing values:")
print(train_df.isnull().sum().sum())

print("\nDuplicate rows:")
print(train_df.duplicated().sum())

sensor_columns = [f'sensor_{i}' for i in range(1, 22)]

print("\nSensor statistics:")
print(train_df[sensor_columns].describe().T)

constant_sensors = [
    col for col in sensor_columns
    if train_df[col].nunique() == 1
]

print("\nConstant sensors:")
print(constant_sensors)

print("\nNumber of constant sensors:", len(constant_sensors))

engine_1 = train_df[train_df['engine_id'] == 1]

print("\nEngine 1 sensor readings:")
print(
    engine_1[['cycle', 'sensor_2', 'sensor_3',
              'sensor_4', 'sensor_9', 'sensor_14',
              'sensor_21']].head(10)
)
print("\nFirst cycle:")
print(engine_1.head(1))

print("\nLast cycle:")
print(engine_1.tail(1))

import plotly.express as px

fig = px.line(
    engine_1,
    x='cycle',
    y=['sensor_3', 'sensor_14', 'sensor_21'],
    facet_col='variable',
    facet_col_wrap=1,
    title='Engine 1 - Sensor Degradation Trends'
)

fig.update_yaxes(matches=None)

fig.show()

last_cycles = train_df.groupby('engine_id')['cycle'].max()

train_df['RUL'] = (
    train_df['engine_id'].map(last_cycles) - train_df['cycle']
)

print("\nRUL values:")
print(train_df[['engine_id', 'cycle', 'RUL']].head(10))

print("\nLast records of Engine 1:")
print(
    train_df[train_df['engine_id'] == 1][
        ['engine_id', 'cycle', 'RUL']
    ].tail()
)
train_df['RUL_capped'] = train_df['RUL'].clip(upper=125)

print("\nCapped RUL values:")
print(
    train_df[['engine_id', 'cycle', 'RUL', 'RUL_capped']].head(10)
)
print("\nRUL distribution:")
print(train_df['RUL_capped'].describe())

print("\nRecords with capped RUL = 125:")
print((train_df['RUL_capped'] == 125).sum())

print("\nRecords with RUL below 125:")
print((train_df['RUL_capped'] < 125).sum())


test_df = pd.read_csv(
    'data/raw/test_FD001.txt',
    sep=r'\s+',
    header=None,
    names=columns
)

print("\nTest dataset:")
print(test_df.head())

print("\nTest dataset shape:", test_df.shape)

print("\nTotal test engines:", test_df['engine_id'].nunique())



rul_df = pd.read_csv(
    'data/raw/RUL_FD001.txt',
    sep=r'\s+',
    header=None,
    names=['actual_RUL']
)

print("\nActual RUL file:")
print(rul_df.head(10))

print("\nRUL file shape:", rul_df.shape)


last_test_cycles = test_df.groupby('engine_id')['cycle'].max()

print("\nLast recorded cycle for each test engine:")
print(last_test_cycles.head(10))

test_summary = pd.DataFrame({
    'last_cycle': last_test_cycles.values,
    'actual_RUL': rul_df['actual_RUL'].values
})

test_summary.index = last_test_cycles.index
test_summary.index.name = 'engine_id'

print("\nTest engine summary:")
print(test_summary.head(10))