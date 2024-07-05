import pandas as pd
import numpy as np

# Sample data loading
data = pd.read_excel('flood_warnings.xlsx', engine='openpyxl')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Assuming data for 2015 is missing, using linear interpolation
data.interpolate(method='time', inplace=True)

# Checking the data after imputation
print(data.head())