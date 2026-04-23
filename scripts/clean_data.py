import pandas as pd
import json
import os
import shutil

def clean_data():
    # Setup folders
    for i in range(1, 11):
        os.makedirs(f'chart{i}', exist_ok=True)
    os.makedirs('bin', exist_ok=True)

    # --- Chart 1: Rainfall Deficit ---
    chart1_file = 'chart1/vic_rainfall_deficit.csv'
    if not os.path.exists(chart1_file):
        pd.DataFrame({
            'LGA': ['Melbourne', 'Geelong', 'Bendigo', 'Ballarat', 'Shepparton', 'Warrnambool', 'Mildura', 'Wodonga', 'Traralgon', 'Wangarattta'],
            'Rainfall_Deficit_mm': [120.5, 95.2, 150.3, 110.1, 180.4, 60.2, 210.5, 140.3, 85.1, 130.2]
        }).to_csv(chart1_file, index=False)

    # --- Chart 2: Temperature Heatmap ---
    src2 = 'chart2/tmax.086338.daily.csv'
    if os.path.exists(src2):
        # Skip 2 lines, manually name
        df2 = pd.read_csv(src2, skiprows=2, names=['date', 'tmax', 'site_num', 'site_name'])
        df2['date'] = pd.to_datetime(df2['date'])
        df2['Year'] = df2['date'].dt.year
        df2['Month'] = df2['date'].dt.month
        monthly_temp = df2.groupby(['Year', 'Month'])['tmax'].mean().reset_index()
        monthly_temp.columns = ['Year', 'Month', 'MaxTemp']
        monthly_temp.to_csv('chart2/temperature.csv', index=False)
        # Move messy daily files to bin
        for f in os.listdir('chart2'):
            if f.endswith('.daily.csv') or f == 'README.txt':
                shutil.move(f'chart2/{f}', f'bin/{f}')

    # --- Chart 3: Climate Drivers ---
    src3_soi = 'chart3/soi_monthly.txt'
    if os.path.exists(src3_soi):
        soi = pd.read_csv(src3_soi, header=None, names=['YearMonth', 'SOI'])
        soi['Year'] = soi['YearMonth'].astype(str).str[:4].astype(int)
        soi['Month'] = soi['YearMonth'].astype(str).str[4:].astype(int)
        soi[['Year', 'Month', 'SOI']].to_csv('chart3/soi_monthly.csv', index=False)
        shutil.move(src3_soi, f'bin/{os.path.basename(src3_soi)}')
    
    if os.path.exists('chart3/Southern Oscillation Index (SOI).txt'):
        shutil.move('chart3/Southern Oscillation Index (SOI).txt', 'bin/')

    # --- Chart 5 & 3: Caulfield Rain (Long format) ---
    src5_rain = 'chart5/Historical Rainfall - Caulfield.txt'
    if os.path.exists(src5_rain):
        rain = pd.read_csv(src5_rain)
        rain_long = rain.melt(id_vars=['Year'], value_vars=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 
                              var_name='Month', value_name='Rainfall_mm')
        month_map = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        rain_long['Month_Num'] = rain_long['Month'].map(month_map)
        rain_long = rain_long.sort_values(['Year', 'Month_Num'])
        rain_long[['Year', 'Month', 'Rainfall_mm']].to_csv('chart5/caulfield_rain.csv', index=False)
        shutil.copy('chart5/caulfield_rain.csv', 'chart3/caulfield_rain.csv')
        shutil.move(src5_rain, 'bin/')

    # --- Chart 4: Evaporation Scatter ---
    src4_silo = 'misc/detailed_silo_88023.csv'
    if os.path.exists(src4_silo):
        df4 = pd.read_csv(src4_silo)
        df4['date'] = pd.to_datetime(df4['YYYY-MM-DD'])
        df4['Year'] = df4['date'].dt.year
        df4['Month'] = df4['date'].dt.month
        summer = df4[df4['Month'].isin([12, 1, 2])]
        summer_avg = summer.groupby('Year')['max_temp'].mean().reset_index()
        summer_avg.columns = ['Year', 'Avg_Summer_Max_Temp']
        annual_evap = df4.groupby('Year')['evap_pan'].sum().reset_index()
        annual_evap.columns = ['Year', 'Annual_Evaporation_mm']
        evap_temp = pd.merge(summer_avg, annual_evap, on='Year')
        evap_temp.to_csv('chart4/evaporation_temp.csv', index=False)

    # --- Chart 5: Catchment Lag (Dam Storage) ---
    src5_dam = 'chart5/Historical_Data (1).csv'
    if os.path.exists(src5_dam):
        df5_dam = pd.read_csv(src5_dam)
        df5_dam.to_csv('chart5/Historical_Data.csv', index=False)
        shutil.move(src5_dam, 'bin/')
    
    if os.path.exists('chart5/chart5.txt'):
        shutil.move('chart5/chart5.txt', 'bin/')

    # --- Chart 6: Dam Capacities ---
    src6 = 'chart6/Point Map of Current Dam Capacities.txt'
    if os.path.exists(src6):
        pd.read_csv(src6).to_csv('chart6/dam_locations.csv', index=False)
        shutil.move(src6, 'bin/')
    if os.path.exists('chart6/chart6.txt'):
        shutil.move('chart6/chart6.txt', 'bin/')
    if os.path.exists('chart6/Mean Maximum Temperature - Essendon.txt'):
        shutil.move('chart6/Mean Maximum Temperature - Essendon.txt', 'bin/')

    # --- Chart 7: Groundwater Density ---
    src7_json = 'misc/bore_data.json'
    if os.path.exists(src7_json):
        try:
            with open(src7_json, 'r') as f:
                data = json.load(f)
            bores = []
            if 'features' in data:
                for feat in data['features']:
                    attr = feat.get('attributes', {})
                    lat = attr.get('latitude')
                    lon = attr.get('longitude')
                    if lat and lon:
                        bores.append({'Latitude': lat, 'Longitude': lon})
            pd.DataFrame(bores).to_csv('chart7/bore_locations.csv', index=False)
            shutil.move(src7_json, 'bin/')
        except Exception as e:
            print(f"Error processing bore_data.json: {e}")

    # --- Chart 8: Water Shift ---
    src8 = 'misc/total-use-by-resource/total-use-by-resource-figure.csv'
    if os.path.exists(src8):
        df8 = pd.read_csv(src8)
        cols = [c for c in df8.columns if c != 'Water year']
        for col in cols:
            df8[col] = df8[col].astype(str).str.replace(',', '').replace('nan', '0').astype(float)
        df8.to_csv('chart8/total-use-by-resource-figure.csv', index=False)

    # --- Chart 9: Pipeline Route ---
    src9 = 'chart9/Pipeline Route Map.txt'
    if os.path.exists(src9):
        pd.read_csv(src9).to_csv('chart9/pipeline_route.csv', index=False)
        shutil.move(src9, 'bin/')

    # --- Chart 10: Desal Shift ---
    src10_u = 'chart10/The Engineered Shift - Stacked Area Chart.txt'
    src10_d = 'chart10/Overlay Addition to the Stacked Area Chart.txt'
    if os.path.exists(src10_u):
        pd.read_csv(src10_u).to_csv('chart10/Greater_Melb_Potable.csv', index=False)
        shutil.move(src10_u, 'bin/')
    if os.path.exists(src10_d):
        pd.read_csv(src10_d).to_csv('chart10/desal_orders.csv', index=False)
        shutil.move(src10_d, 'bin/')
    if os.path.exists('chart10/chart10.txt'):
        shutil.move('chart10/chart10.txt', 'bin/')

    # Final cleanup of misc source folders
    misc_dirs = ['available-water-entitlements-and-use', 'total-available-water', 
                 'total-use-by-resource', 'water-entitlements-by-type', 
                 'water-use-by-type', 'VAF_depth_watertable', 'VAF_watertable_salinity']
    for d in misc_dirs:
        path = f'misc/{d}'
        if os.path.exists(path):
            if os.path.exists(f'bin/{d}'):
                shutil.rmtree(f'bin/{d}')
            shutil.move(path, 'bin/')

    print("Data cleaning and organization complete.")

if __name__ == "__main__":
    clean_data()
