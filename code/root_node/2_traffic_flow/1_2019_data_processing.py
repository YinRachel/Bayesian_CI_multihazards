import pandas as pd

# 
two_area_stations = pd.read_excel('./original_data/station_name.xlsx')
london_stations = pd.read_excel('./original_data/2019_Station Footfall.xlsx')

two_area_stations['station name'] = two_area_stations['station name'].str.lower()
london_stations['Station'] = london_stations['Station'].str.lower()

london_stations.rename(columns={'Station': 'station name'}, inplace=True)

result_2019 = pd.merge(two_area_stations, london_stations, on='station name', how='left')
# result_2022.to_excel('2022_matched_stations.xlsx', index = False)
result_2019['TravelDate'] = pd.to_datetime(result_2019['TravelDate'],format='%Y%m%d')
result_2019_sorted = result_2019.sort_values(by='TravelDate')

# delete empty
result_2019_sorted.dropna(subset=['TravelDate'], inplace=True)

result_2019_sorted.to_excel('./matched_data/2019_sorted_stations.xlsx', index = False)



# print(result_2022_sorted.iloc[15453])

