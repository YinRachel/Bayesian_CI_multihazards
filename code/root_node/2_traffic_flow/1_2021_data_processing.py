import pandas as pd

# 
two_area_stations = pd.read_excel('./original_data/station_name.xlsx')
london_stations = pd.read_excel('./original_data/2021_Station Footfall.xlsx')

two_area_stations['station name'] = two_area_stations['station name'].str.lower()
london_stations['Station'] = london_stations['Station'].str.lower()

london_stations.rename(columns={'Station': 'station name'}, inplace=True)

result_2021 = pd.merge(two_area_stations, london_stations, on='station name', how='left')
# result_2022.to_excel('2022_matched_stations.xlsx', index = False)
result_2021['TravelDate'] = pd.to_datetime(result_2021['TravelDate'],format='%Y%m%d')
result_2021_sorted = result_2021.sort_values(by='TravelDate')

# delete empty
result_2021_sorted.dropna(subset=['TravelDate'], inplace=True)

result_2021_sorted.to_excel('./matched_data/2021_sorted_stations.xlsx', index = False)



# print(result_2022_sorted.iloc[15453])

