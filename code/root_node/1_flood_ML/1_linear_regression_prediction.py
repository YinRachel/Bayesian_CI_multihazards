import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import calendar

data = pd.read_excel('flood_warnings.xlsx', engine='openpyxl')

#print(data.head())

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

# print(data.head())

# predict time
predict_month = [2024,11]

# red warning prediction

X = data[['Year','Month']]
y_red = data['Severe Flood Warnings']

X_train, X_test, y_red_train, y_red_test = train_test_split(X,y_red,test_size=0.2,random_state=42)

red_model = LinearRegression()
red_model.fit(X_train, y_red_train)
# 使用pandas DataFrame进行预测，确保列名与训练数据一致

prediction_red_df = pd.DataFrame([predict_month], columns=['Year', 'Month'])

prediction_red = red_model.predict(prediction_red_df)

rounded_prediction_red = np.round(prediction_red[0])


# yellow warning prediction

y_yellow = data['Flood Warnings']

X_train, X_test, y_yellow_train, y_yellow_test = train_test_split(X,y_yellow,test_size=0.2,random_state=42)

yellow_model = LinearRegression()
yellow_model.fit(X_train, y_yellow_train)

# 使用pandas DataFrame进行预测，确保列名与训练数据一致

prediction_yellow_df = pd.DataFrame([predict_month], columns=['Year', 'Month'])

prediction_yellow = yellow_model.predict(prediction_yellow_df)

rounded_prediction_yellow = np.round(prediction_yellow[0])



# green warning prediction

y_green = data['Flood Alert']

X_train, X_test, y_green_train, y_green_test = train_test_split(X,y_green,test_size=0.2,random_state=42)

green_model = LinearRegression()
green_model.fit(X_train, y_green_train)

# 使用pandas DataFrame进行预测，确保列名与训练数据一致

prediction_green_df = pd.DataFrame([predict_month], columns=['Year', 'Month'])

prediction_green = green_model.predict(prediction_green_df)

rounded_prediction_green = np.round(prediction_green[0])

# get month name
get_month_name = calendar.month_name[predict_month[1]]


print(f'the amount of severe flood warnings in {get_month_name} {predict_month[0]} is {rounded_prediction_red}')
print(f'the amount of flood warnings in {get_month_name} {predict_month[0]} is {rounded_prediction_yellow}')
print(f'the amount of flood alert in {get_month_name} {predict_month[0]} is {rounded_prediction_green}')