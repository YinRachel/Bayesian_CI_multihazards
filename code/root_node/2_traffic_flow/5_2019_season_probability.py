import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans

# 文件夹路径
folder_path = './2019_data'

# 自定义阈值
# low_threshold_customize = 3500
# high_threshold_customize = 10000

two_borough_df = pd.read_excel('./matched_data/2019_sorted_stations.xlsx')

data_borough = two_borough_df['EntryTapCount'].values.reshape(-1,1)

kmeans_borough = KMeans(n_clusters=3, random_state=0).fit(data_borough)

centers_borough = kmeans_borough.cluster_centers_.flatten()

centers_borough.sort()

low_threshold_borough = centers_borough[0]
high_threshold_borough = centers_borough[2]



# 创建一个空的 DataFrame 用于汇总数据
columns = ['station', 'season', 'low', 'medium', 'high']
summary_df_customize = pd.DataFrame(columns=columns)

# 定义一个函数来确定季节
def get_season(month):
    if month in [9, 10, 11]:
        return 'autumn'
    elif month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    else:
        return 'summer'

# 遍历目录中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        # 读取每个地铁站的 Excel 文件
        station_path = os.path.join(folder_path, file_name)
        station_data = pd.read_excel(station_path)
        
        # 将日期转换为月份并确定季节
        station_data['Month'] = pd.to_datetime(station_data['TravelDate']).dt.month
        station_data['season'] = station_data['Month'].apply(get_season)
        
        # 对每个季节计算流量等级的概率
        for season in station_data['season'].unique():
            season_mask = station_data['season'] == season
            station_data.loc[season_mask, 'trafficLevel'] = station_data.loc[season_mask, 'EntryTapCount'].apply(
                lambda x: 'high' if x >= high_threshold_borough else ('medium' if x > low_threshold_borough else 'low')
            )
            traffic_level_counts = station_data.loc[season_mask, 'trafficLevel'].value_counts(normalize=True)
            
            # 为当前地铁站准备一行数据
            station_name = file_name.replace('_data.xlsx', '').replace('_', ' ')
            station_row = {'station': station_name, 'season': season}
            
            # 保证每个流量等级的概率都被记录
            for level in ['low', 'medium', 'high']:
                station_row[level] = traffic_level_counts.get(level, 0.0)
            
            # 将当前地铁站的数据追加到汇总 DataFrame
            summary_df_customize = summary_df_customize._append(station_row, ignore_index=True)

# 打印汇总的DataFrame
# print(summary_df_customize)

# 按季节分组，并计算不同季节的平均高中低概率
numeric_columns = summary_df_customize.select_dtypes(include=[np.number]).columns
seasonal_probability = summary_df_customize.groupby('season')[numeric_columns].mean().reset_index()
print(seasonal_probability)


