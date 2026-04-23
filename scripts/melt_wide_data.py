import pandas as pd
import os

def melt_remaining_wide_data():
    # 1. Melt Chart 5 Historical Data
    c5_path = 'data/final/chart5_Historical_Data.csv'
    if os.path.exists(c5_path):
        df5 = pd.read_csv(c5_path)
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
        # Melt months into a single column
        df5_long = df5.melt(id_vars=['Year'], value_vars=months, 
                            var_name='Month', value_name='Storage_Percentage')
        # Map months to numbers for easy sorting later
        month_map = {m: i+1 for i, m in enumerate(months)}
        df5_long['Month_Num'] = df5_long['Month'].map(month_map)
        df5_long = df5_long.sort_values(['Year', 'Month_Num'])
        df5_long.to_csv(c5_path, index=False)
        # Update raw folder as well
        df5_long.to_csv('data/raw/chart5/Historical_Data.csv', index=False)
        print("Melted Chart 5 (Historical Reservoir Levels) to Long format.")

    # 2. Melt Chart 8 Water Usage Data
    c8_path = 'data/final/chart8_total-use-by-resource-figure.csv'
    if os.path.exists(c8_path):
        df8 = pd.read_csv(c8_path)
        resource_cols = [c for c in df8.columns if c != 'Water year']
        df8_long = df8.melt(id_vars=['Water year'], value_vars=resource_cols, 
                            var_name='Resource_Type', value_name='Volume_ML')
        df8_long.to_csv(c8_path, index=False)
        # Update raw folder as well
        df8_long.to_csv('data/raw/chart8/total-use-by-resource-figure.csv', index=False)
        print("Melted Chart 8 (Water Usage by Resource) to Long format.")

if __name__ == "__main__":
    melt_remaining_wide_data()
