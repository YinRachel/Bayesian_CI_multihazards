import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import os

## define threshold through london all stations
all_stations_df = pd.read_excel('./original_data/2021_Station Footfall.xlsx')

# # 提取EntryTapCount数据用于聚类
traffic_data = all_stations_df['EntryTapCount'].values.reshape(-1, 1)

# # 使用 KMeans 定义临界值
kmeans = KMeans(n_clusters=3, random_state=0).fit(traffic_data)
centers = kmeans.cluster_centers_.flatten()
centers.sort()  # 确保临界值按顺序排列：低、中、高

# define threshold
low_threshold_all = centers[0]
high_threshold_all = centers[2]

# 文件夹路径
folder_path = './2021_data'

# 创建一个空的 DataFrame 用于汇总数据
columns = ['station', 'low', 'medium', 'high']
summary_df_all = pd.DataFrame(columns=columns)

for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        # 读取每个地铁站的 Excel 文件
        station_path = os.path.join(folder_path, file_name)
        station_data = pd.read_excel(station_path)
        
        # 计算每个流量等级的概率
        station_data['trafficLevel'] = station_data['EntryTapCount'].apply(
            lambda x: 'high' if x >= high_threshold_all else ('medium' if x > low_threshold_all else 'low')
        )
        traffic_level_counts = station_data['trafficLevel'].value_counts(normalize=True)
        
        # 为当前地铁站准备一行数据
        station_name = file_name.replace('_data.xlsx', '').replace('_', ' ')
        station_row = {'station': station_name}
        
        # 保证每个流量等级的概率都被记录
        for level in ['low', 'medium', 'high']:
            station_row[level] = traffic_level_counts.get(level, 0.0)
        
        # 将当前地铁站的数据追加到汇总 DataFrame
        summary_df_all = summary_df_all._append(station_row, ignore_index=True)

# print(summary_df)

average_low_all = summary_df_all['low'].mean()
average_medium_all = summary_df_all['medium'].mean()
average_high_all = summary_df_all['high'].mean()

average_result_all = {
    'low':average_low_all,
    'medium':average_medium_all,
    'high':average_high_all
}



## define threshold through the stations in two areas
two_borough_df = pd.read_excel('./matched_data/2021_sorted_stations.xlsx')

data_borough = two_borough_df['EntryTapCount'].values.reshape(-1,1)

kmeans_borough = KMeans(n_clusters=3, random_state=0).fit(data_borough)

centers_borough = kmeans_borough.cluster_centers_.flatten()

centers_borough.sort()

low_threshold_borough = centers_borough[0]
high_threshold_borough = centers_borough[2]

## customize threshold
low_threshold_customize = 3500
high_threshold_customize = 10000


# print(low_threshold)
# print(high_threshold)

summary_df_borough = pd.DataFrame(columns=columns)

# 遍历目录中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        # 读取每个地铁站的 Excel 文件
        station_path = os.path.join(folder_path, file_name)
        station_data = pd.read_excel(station_path)
        
        # 计算每个流量等级的概率
        station_data['trafficLevel'] = station_data['EntryTapCount'].apply(
            lambda x: 'high' if x >= high_threshold_borough else ('medium' if x > low_threshold_borough else 'low')
        )
        traffic_level_counts = station_data['trafficLevel'].value_counts(normalize=True)
        
        # 为当前地铁站准备一行数据
        station_name = file_name.replace('_data.xlsx', '').replace('_', ' ')
        station_row = {'station': station_name}
        
        # 保证每个流量等级的概率都被记录
        for level in ['low', 'medium', 'high']:
            station_row[level] = traffic_level_counts.get(level, 0.0)
        
        # 将当前地铁站的数据追加到汇总 DataFrame
        summary_df_borough = summary_df_borough._append(station_row, ignore_index=True)

# print(summary_df)

average_low_borough = summary_df_borough['low'].mean()
average_medium_borough = summary_df_borough['medium'].mean()
average_high_borough = summary_df_borough['high'].mean()

average_result_borough = {
    'low':average_low_borough,
    'medium':average_medium_borough,
    'high':average_high_borough
}



summary_df_customize = pd.DataFrame(columns=columns)

# 遍历目录中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        # 读取每个地铁站的 Excel 文件
        station_path = os.path.join(folder_path, file_name)
        station_data = pd.read_excel(station_path)
        
        # 计算每个流量等级的概率
        station_data['trafficLevel'] = station_data['EntryTapCount'].apply(
            lambda x: 'high' if x >= high_threshold_customize else ('medium' if x > low_threshold_customize else 'low')
        )
        traffic_level_counts = station_data['trafficLevel'].value_counts(normalize=True)
        
        # 为当前地铁站准备一行数据
        station_name = file_name.replace('_data.xlsx', '').replace('_', ' ')
        station_row = {'station': station_name}
        
        # 保证每个流量等级的概率都被记录
        for level in ['low', 'medium', 'high']:
            station_row[level] = traffic_level_counts.get(level, 0.0)
        
        # 将当前地铁站的数据追加到汇总 DataFrame
        summary_df_customize = summary_df_customize._append(station_row, ignore_index=True)

# print(summary_df)

average_low_customize = summary_df_customize['low'].mean()
average_medium_customize = summary_df_customize['medium'].mean()
average_high_customize = summary_df_customize['high'].mean()

average_result_customize = {
    'low':average_low_customize,
    'medium':average_medium_customize,
    'high':average_high_customize
}

print('all london station Kmeans threshold',average_result_all)
print('two borough Kmeans threshold',average_result_borough)
print('customize threshold',average_result_customize)