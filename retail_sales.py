# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import datetime
import dateutil

# Add prior month's unrevised data and estimates:

month = "2021-05-01"
rpt_list = ["retail sales", "retail sales ex. autos"]
prior_unrevised = [0.0, -0.8]
estimate = [-0.5, 0.3]

# Code for API pull from Census Bureau

time = pd.to_datetime(month, format ='%Y-%m')
m = [month, month]
estimates = pd.DataFrame(zip(m, rpt_list, prior_unrevised, estimate), columns=["time", "report", "prior_unrevised", "estimate"])

data_from = "2012-01"
base_url = 'https://api.census.gov/data/timeseries/eits/marts?get=data_type_code,seasonally_adj,category_code,cell_value,error_data&for=us:*&time=from+{}'.format(data_from)

response = requests.get(base_url)
data = response.json()
df2 = pd.DataFrame(data[1:], columns = data[0])
df2["time"] = pd.to_datetime(df2["time"], format = '%Y-%m')
df2["cell_value"] = [float(str(i).replace(",","")) for i in df2["cell_value"]]
df2["cell_value"] = df2["cell_value"].map(lambda x: float(x))
df2["month"] = df2["time"].map(lambda x: x.strftime("%B"))

# Report codes for headline and ex.autos m/m percent change
report = ["retail sales", "retail sales ex. autos"]
data_type_code = ["MPCSM", "MPCSM"]
category_code = ["44X72", "44Y72"]
seasonally_adj = ["yes", "yes"]
df3 = pd.DataFrame((zip(report, data_type_code, category_code, seasonally_adj)))
df3.columns = ["report", "data_type_code","category_code", "seasonally_adj"]

retail_sales = pd.merge(df3, df2, how = "right", left_on = ["data_type_code", "category_code", "seasonally_adj"], right_on = ["data_type_code", "category_code", "seasonally_adj"])

df2

current_month = retail_sales[retail_sales["time"] == month]
current_month = pd.merge(estimates, current_month, how = "left", left_on = "report", right_on = "report").drop(columns = ["time_y", "data_type_code", "seasonally_adj", "category_code", "error_data", "us"])

headline = retail_sales[retail_sales["report"] == "retail sales"].sort_values(by = "time", ascending=False).drop(columns = ["data_type_code", "seasonally_adj", "category_code", "error_data", "us"])

sales_ex_autos = retail_sales[retail_sales["report"] == "retail sales ex. autos"].sort_values(by = "time", ascending=False).drop(columns = ["data_type_code", "seasonally_adj", "category_code", "error_data", "us"])

# Monthly Reports

current_month # compared to estimates and prior

headline

sales_ex_autos