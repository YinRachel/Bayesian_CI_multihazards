import pandas as pd
import numpy as np
import calendar

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

predict_target_year = [2024,2025]
predict_target_month = [9,10,11,12,1,2]
predict_target_season = ['Autumn','Winter']

def process_data(filename):

    data = pd.read_excel('flood_warnings.xlsx', engine='openpyxl')

    # 假设您的日期列名为"Date"
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month

    def get_season(month):
        if 3 <= month <= 5:
            return 'Spring'
        elif 6 <= month <= 8:
            return 'Summer'
        elif 9 <= month <= 11:
            return 'Autumn'
        else:
            return 'Winter'

    data['Season'] = data['Month'].apply(get_season)

    data = data.drop(columns=['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10'])
    return data

data = process_data('flood_warnings.xlsx')
# print(data.head(12))

# 假设data已加载并进行了预处理
X = data[['Year', 'Month', 'Season']]  # 特征
y = data[['Severe Flood Warnings', 'Flood Warnings', 'Flood Alert']]  # 目标

# 对季节列进行独热编码
column_transformer = ColumnTransformer(
    [('season_encoder', OneHotEncoder(), ['Season'])],
    remainder='passthrough'
)

# 模型
model = Pipeline([
    ('encoder', column_transformer),
    ('regressor', RandomForestRegressor(n_estimators=100))
])

# 使用所有可用数据进行训练
model.fit(X, y)

## predict winter
# 预测2024年12月、2025年1月和2月

def process_winter_data(year, month, season):
        years = [year[0]] * 1 + [year[1]] * 2
        months = [month[i] for i in [3,4,5]]
        seasons = [season[1]] * 3
        future_months = pd.DataFrame({
            'Year':years,
            'Month':months,
            'Season':seasons
        })
        return future_months

winter_dataframe = process_winter_data(predict_target_year,predict_target_month,predict_target_season)

get_month_name = [calendar.month_name[i] for i in predict_target_month]

def get_winter(winter_dataframe):

    # 假设模型已训练，预测未来值
    winter_future_predictions = model.predict(winter_dataframe)

    # 将预测结果转换为概率
    predicted_totals = winter_future_predictions.sum(axis=1)
    probabilities = winter_future_predictions / predicted_totals[:, None]

    formatted_probabilities = [[f"{num:.3f}" for num in row] for row in probabilities]

    print(f'the probability of severe flooding in {get_month_name[3]} is {formatted_probabilities[0][0]}')
    print(f'the probability of flooding warning in {get_month_name[3]} is {formatted_probabilities[0][1]}')
    print(f'the probability of flooding alert in {get_month_name[3]} is {formatted_probabilities[0][2]}')

    average_probabilities = np.mean(probabilities, axis=0)

    formatted_average_probability = [f"{num:.4f}" for num in average_probabilities ]

    print(f'In winter, the probability of severe flooding is {formatted_average_probability[0]}, the probability of flooding warning is {formatted_average_probability[1]}, the probability of flooding alert is {formatted_average_probability[2]}')
    return formatted_average_probability

winter_probability = get_winter(winter_dataframe)

def process_autumn_data(year, month, season):
    years = [year[0]] *3
    months = [month[i] for i in [0,1,2]]
    seasons = [season[0]] * 3
    future_month = pd.DataFrame({
        'Year': years,
        'Month':months,
        'Season':seasons
    })
    return future_month

autumn_dataframe = process_autumn_data(predict_target_year,predict_target_month,predict_target_season)

def get_autumn_probability(autumn_dataframe):
    autumn_furture_prediction = model.predict(autumn_dataframe)
    predicted_totals = autumn_furture_prediction.sum(axis=1)
    probability = autumn_furture_prediction / predicted_totals[:,None]
    average_probability = np.mean(probability,axis = 0)
    formatted_average = [f"{i:.4f}" for i in average_probability]
    print(f'In Autumn, the probability of severe flooding is {formatted_average[0]}, the probability of flooding warning is {formatted_average[1]}, the probability of flooding alert is {formatted_average[2]}')
    return formatted_average

autumn_probability = get_autumn_probability(autumn_dataframe)

winter_probability_float = np.array(winter_probability, dtype=float)
autumn_probability_float = np.array(autumn_probability, dtype=float)

average_two_season = (winter_probability_float + autumn_probability_float) / 2
print(average_two_season)

# trend of each year
# alternative methods 
# list of options 