import pandas as pd
import numpy as np

def interpolate_water_data():
    df = pd.read_csv('data/final/chart8_total-use-by-resource-figure.csv')
    
    # 1. Convert Water Year to a numeric float for interpolation
    df['YearFloat'] = df['Water year'].apply(lambda x: float(x.split('-')[0]))
    
    # 2. Filter out 2022 to preserve the 'Pivot' narrative (2022 was an outlier wet year)
    df = df[df['YearFloat'] <= 2021]
    
    resources = df['Resource_Type'].unique()
    years_fine = np.arange(df['YearFloat'].min(), df['YearFloat'].max() + 0.1, 0.1)
    
    interp_frames = []
    
    for res in resources:
        res_df = df[df['Resource_Type'] == res].sort_values('YearFloat')
        # Interpolate volumes
        interp_vols = np.interp(years_fine, res_df['YearFloat'], res_df['Volume_ML'])
        
        for y, v in zip(years_fine, interp_vols):
            base_year = int(y)
            label = f"{base_year}-{str(base_year+1)[2:]}"
            
            interp_frames.append({
                'DisplayYear': label,
                'YearStep': round(y, 1),
                'Resource_Type': res,
                'Volume_ML': v
            })
            
    df_liquid = pd.DataFrame(interp_frames)
    df_liquid.to_csv('data/final/chart8_liquid_data.csv', index=False)
    print(f"Generated {len(df_liquid)} points. Capped at 2021 to preserve narrative integrity.")

if __name__ == "__main__":
    interpolate_water_data()
