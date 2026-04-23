import pandas as pd
import json
import os

def final_polish():
    # 1. Fix Wangaratta typo in Chart 1
    chart1_path = 'chart1/vic_rainfall_deficit.csv'
    if os.path.exists(chart1_path):
        df1 = pd.read_csv(chart1_path)
        df1['LGA'] = df1['LGA'].replace('Wangarattta', 'Wangaratta')
        df1.to_csv(chart1_path, index=False)
        print("Fixed typo in Chart 1.")

    # 2. Filter Bores to Victoria only for Chart 7 (Storytelling Rigor)
    # Victoria bounds: Lat [-39.2, -34.0], Lon [140.9, 150.0]
    chart7_path = 'chart7/bore_locations.csv'
    if os.path.exists(chart7_path):
        df7 = pd.read_csv(chart7_path)
        vic_df7 = df7[
            (df7['Latitude'] <= -34.0) & (df7['Latitude'] >= -39.2) &
            (df7['Longitude'] >= 140.9) & (df7['Longitude'] <= 150.0)
        ]
        vic_df7.to_csv(chart7_path, index=False)
        print(f"Filtered Chart 7 to Victoria. Rows reduced from {len(df7)} to {len(vic_df7)}.")

if __name__ == "__main__":
    final_polish()
