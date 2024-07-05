import pandas as pd

sorted_stations_2019 = pd.read_excel('./matched_data/2019_sorted_stations.xlsx')

unique_stations = sorted_stations_2019['station name'].unique()

for station in unique_stations:
    station_data = sorted_stations_2019[sorted_stations_2019['station name']==station]
    filename = f"{station.replace(' ','_')}_data.xlsx"
    station_data.to_excel(f'./2019_data/{filename}',index = False)
