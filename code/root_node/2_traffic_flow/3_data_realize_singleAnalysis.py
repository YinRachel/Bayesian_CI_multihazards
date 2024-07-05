import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

all_stations_df = pd.read_excel('./original_data/2022_Station Footfall.xlsx')
aldgate_data = pd.read_excel('./2022_data/aldgate_east_data.xlsx')

# get_quantiles = aldgate_data['EntryTapCount'].quantile([0.25,0.5,0.75])

# low_threshold = get_quantiles[0.25]
# high_threshold = get_quantiles[0.75]
# # print(get_quantiles)

# conditions = [
#     (aldgate_data['EntryTapCount']<=low_threshold),
#     (aldgate_data['EntryTapCount']>=low_threshold)&(aldgate_data['EntryTapCount']<=high_threshold),
#     (aldgate_data['EntryTapCount']>=high_threshold)
# ]

# categories = ['low','medium','high']

# aldgate_data['trafficLevel'] = np.select(conditions,categories)

# print(aldgate_data.head(20))

# X = aldgate_data['EntryTapCount'].values.reshape(-1,1)
# kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# aldgate_data['Cluster'] = kmeans.labels_

# centers = kmeans.cluster_centers_

# traffic_levels = ['low','medium','high']
# aldgate_data['trafficLevel'] =aldgate_data['Cluster'].apply(lambda x: traffic_levels[np.argsort(centers, axis=0).flatten()[x]])

# print(aldgate_data.head(20))

traffic_data = all_stations_df['EntryTapCount'].values.reshape(-1, 1)

# 使用 KMeans 确定临界值，我们选择3个聚类中心
kmeans = KMeans(n_clusters=3, random_state=0).fit(traffic_data)
centers = kmeans.cluster_centers_

# 确定临界值
low_threshold = np.min(centers)
high_threshold = np.max(centers)

print(low_threshold)
print(high_threshold)

# 分类每天的客流量
all_stations_df['TrafficLevel'] = all_stations_df['EntryTapCount'].apply(
    lambda x: 'High' if x >= high_threshold else ('Medium' if x > low_threshold else 'Low')
)

# print(all_stations_df.head())

conditions = [
    (aldgate_data['EntryTapCount']<=low_threshold),
    (aldgate_data['EntryTapCount']>=low_threshold)&(aldgate_data['EntryTapCount']<=high_threshold),
    (aldgate_data['EntryTapCount']>=high_threshold)
]

categories = ['low','medium','high']

aldgate_data['trafficLevel'] = np.select(conditions,categories)

traffic_level_counts = aldgate_data['trafficLevel'].value_counts(normalize=True)


print(aldgate_data.head(20))
print(traffic_level_counts)