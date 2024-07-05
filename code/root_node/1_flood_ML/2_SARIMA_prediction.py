import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pmdarima as pm

data = pd.read_excel('flood_warnings.xlsx', engine='openpyxl')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date',inplace=True)


y_severe = data['Severe Flood Warnings']

set_month = '2024-11'

model = pm.auto_arima(y_severe, seasonal=True, m=12, stepwise=True, suppress_warnings=True, error_action='ignore', trace=True)

future_months = pd.date_range(start=data.index[-1] + pd.offsets.MonthEnd(1), end=set_month, freq='M')
n_periods = len(future_months)


future_severe = model.predict(n_periods = n_periods)

# predict_severe = future_severe[-1]
print(future_severe.shape)