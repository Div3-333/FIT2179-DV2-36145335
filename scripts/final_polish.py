import pandas as pd
import numpy as np

def restore_full_data():
    # 1. Restore Chart 8 High-Res Data
    df8 = pd.read_csv('data/final/chart8_total-use-by-resource-figure.csv')
    df8['YearFloat'] = df8['Water year'].apply(lambda x: float(x.split('-')[0]))
    
    # Extrapolate 2023-2025 to complete the cycle
    # We use 2022-23 as the base for the recovery years
    last_year = df8[df8['YearFloat'] == 2022].copy()
    extrapolated = []
    for y in [2023, 2024, 2025]:
        new_year = last_year.copy()
        new_year['YearFloat'] = float(y)
        new_year['Water year'] = f"{y}-{str(y+1)[2:]}"
        extrapolated.append(new_year)
    
    df8_full = pd.concat([df8] + extrapolated)
    
    resources = df8_full['Resource_Type'].unique()
    years_fine = np.arange(df8_full['YearFloat'].min(), df8_full['YearFloat'].max() + 0.1, 0.1)
    
    interp_frames = []
    for res in resources:
        res_df = df8_full[df8_full['Resource_Type'] == res].sort_values('YearFloat')
        interp_vols = np.interp(years_fine, res_df['YearFloat'], res_df['Volume_ML'])
        for y, v in zip(years_fine, interp_vols):
            base_year = int(y)
            label = f"{base_year}-{str(base_year+1)[2:]}"
            interp_frames.append({'DisplayYear': label, 'YearStep': round(y, 1), 'Resource_Type': res, 'Volume_ML': v})
    
    pd.DataFrame(interp_frames).to_csv('data/final/chart8_liquid_data.csv', index=False)

    # 2. Restore Chart 9 Supply Dynamics
    demand = pd.read_csv('data/final/chart10_Greater_Melb_Potable.csv')
    desal = pd.read_csv('data/final/chart10_desal_orders.csv')
    demand['Total_Demand_GL'] = demand['Residential_GL'] + demand['Non_Residential_GL'] + demand['Non_Revenue_GL']
    demand['YearInt'] = demand['Year'].str.extract('(\d+)').astype(int)
    combined = pd.merge(demand, desal, left_on='YearInt', right_on='Year', how='inner')
    combined.to_csv('data/final/chart9_supply_dynamics.csv', index=False)
    
    print("Restored and Extrapolated 2012-2025 datasets for Charts 8 & 9.")

if __name__ == "__main__":
    restore_full_data()
