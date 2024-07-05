import pandas as pd

# 
two_area_stations = pd.read_excel('./original_data/station_name.xlsx')
london_stations = pd.read_excel('./original_data/2020_Station Footfall.xlsx')

two_area_stations['station name'] = two_area_stations['station name'].str.lower()
london_stations['Station'] = london_stations['Station'].str.lower()

london_stations.rename(columns={'Station': 'station name'}, inplace=True)

result_2020 = pd.merge(two_area_stations, london_stations, on='station name', how='left')
# result_2022.to_excel('2022_matched_stations.xlsx', index = False)
result_2020['TravelDate'] = pd.to_datetime(result_2020['TravelDate'],format='%Y%m%d')
result_2020_sorted = result_2020.sort_values(by='TravelDate')

# delete empty
result_2020_sorted.dropna(subset=['TravelDate'], inplace=True)

result_2020_sorted.to_excel('./matched_data/2020_sorted_stations.xlsx', index = False)



# print(result_2022_sorted.iloc[15453])

