import pandas as pd

# Load drivers
df_drivers = pd.read_csv('data/drivers.parquet')
print("Drivers columns:", df_drivers.columns.tolist())
print(df_drivers.head())

# Load laps
df_laps = pd.read_csv('data/laps.parquet')
print("Laps columns:", df_laps.columns.tolist())

# Find the best lap for each driver
best_laps = df_laps.groupby('driver_number')['lap_duration'].min().reset_index()
best_laps = best_laps.sort_values('lap_duration')

# Merge with drivers to get names
best_laps = best_laps.merge(df_drivers[['driver_number', 'name_acronym']], on='driver_number', how='left')

# Top 10
top_10 = best_laps.head(10)
print("Top 10 fastest drivers:")
for idx, row in top_10.iterrows():
    print(f"{idx+1}. {row['name_acronym']} - {row['lap_duration']} seconds")