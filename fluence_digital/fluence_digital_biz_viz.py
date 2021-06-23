#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('ipython jupyter nbconvert fluence-digital-biz-viz.ipynb --fluence-digital-biz-viz.py')


# In[1]:


get_ipython().system('pip install snowflake-sqlalchemy')


# In[2]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import numpy as np 
import pandas as pd 

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px

import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)


# In[3]:


url = URL(
    account = '',
    user = '',
    password = '',
    warehouse = '',
    database = '',
    schema = '')

engine = create_engine(url)

connection = engine.connect()


# In[4]:


#Pull necessary tables

query1 = 'select * from  "CASESTUDY"."CASESTUDY_MINDY"."METRIC"'
metric_df = pd.read_sql_query(query1, connection)
metric_df

query2 = 'select "a"."settlement_time", "a"."actual_price", "f"."p50" as "fluence_p50", "m"."p50" as "market_p50", abs("f"."p50"-"a"."actual_price") as "f_diff_a", abs("m"."p50"-"a"."actual_price") as "m_diff_a" from "CASESTUDY"."CASESTUDY_MINDY"."actual_prices" as "a" join "CASESTUDY"."CASESTUDY_MINDY"."fluence_forecast" as "f" on ("a"."settlement_time" = "f"."settlement_time") join "CASESTUDY"."CASESTUDY_MINDY"."market_forecast" as "m" on ("a"."settlement_time" = "m"."settlement_time") '
viz_df = pd.read_sql_query(query2, connection)
viz_df

query3 = 'select * from  "CASESTUDY"."CASESTUDY_MINDY"."MONTH_AGGREGATE"'
viz_df_month = pd.read_sql_query(query3, connection)
viz_df_month

query4 = 'select * from  "CASESTUDY"."CASESTUDY_MINDY"."DAY_AGGREGATE"'
viz_df_day = pd.read_sql_query(query4, connection)
viz_df_day


# ## BAN's (Key Metrics to Determine Best Forecast).
# 
# In a usual dashboard, BAN's are key metrics displayed at top since these are most important to the end user.

# In[5]:


metric_df


# # VISUALIZATIONS
# 
# Plotly graphs offer interactive, scientific data visualizations to your Web browser. Best features are the zoom-pan-hover controls located at the top right corner of each visualization. Other options include downloading plot, autoscaling, resetting axes, viewing with toggle spike lines, and specifying hover information. Feel free to play around with your visualizalizations! At the same time I'll offer recommendations for best user experience.
# 
# I chose Plotly over Bokeh because it has more built-in interactivity options and cleaner look for end user.
# 
# Below are five different ways I thought would help to best answer whose forecast is better: Fluence or market operators. Looking at forecasts' difference to actual as well as comparing forecasts' drift from actual both help answer which forecast predicted better. Also, looking at time series data in aggregate allows you to pick up trends, spikes and dips much quicker, which leads to faster business decision-making. 

# ## Viz 1 : Differences from Actual (Fluence vs Market)
# 
# The graph with values closest to 0 is the best forecast.
# 
# For interactivity:
# You can use buttons and range slider to narrow or expand time view. 
# Also, hovering over data points show you specific time, line and $/kWh values.
# 
# Recommendation: To get the best experience a highly recommend clicking on "Compare data on hover" button to see both fluence and market data points at the same time stamp.

# In[6]:


fig = px.line(viz_df, x='settlement_time', y=viz_df.columns[4:], title='Differences from Actual: Fluence vs Market')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=.00125, label="1h", step="hour", stepmode="backward"),
            dict(count=.03, label="1d", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward")
           
        ])
    )
)

fig.update_layout(yaxis_title= "$/kWh")    

fig.show()


# ## Viz 2: Forecasts Against Actual Prices
# 
# Closer the graph  is to the actual price line, the better the forecast is.
# 
# For interactivity: You can use buttons and range slider to narrow or expand time view. Also, hovering over data points show you specific time, line and $/kWh values.)
# 
# Recommendation: To get the best experience a highly recommend clicking on "Compare data on hover" button to see actual, fluence and market data points at the same time stamp.

# In[7]:


fig = px.line(viz_df, x='settlement_time', y=viz_df.columns[1:4], title = "Forecasts Against Actual Prices")

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=.00125, label="1h", step="hour", stepmode="backward"),
            dict(count=.03, label="1d", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward")
            
        ])
    )
)

fig.update_layout(yaxis_title = "$/kWh")
 
fig.show()


# ## Viz 3: Monthly Level
# 
# (While pressing on the graph and sliding your mouse to the right or left allows you to zoom in on the graph. Click on "Reset axes" to go back to original view.)
# 
# Recommendation: To get the best experience a highly recommend clicking on "Compare data on hover" button to see actual, fluence and market data points at the same time stamp. Also, clicking on "Toggle Spike Lines" helps you immediately see what x- and y-values are used as coordinates when hovering.

# In[8]:


fig = px.line(viz_df_month, x='settlement_time', y=viz_df.columns[1:4], title = "Monthly Forecasts Against Actual Prices")

fig.update_layout(yaxis_title = "$/kWh")
 
fig.show()


# ## Viz 4: Daily Level
# 
# (While pressing on the graph and sliding your mouse to the right or left allows you to zoom in on the graph. Click on "Reset axes" to go back to original view.)
# 
# Recommendation: To get the best experience a highly recommend clicking on "Compare data on hover" button to see actual, fluence and market data points at the same time stamp. Also, clicking on "Toggle Spike Lines" help you immediately see what x- and y-values are used as coordinates when hovering.

# In[9]:


fig = px.line(viz_df_day, x='settlement_time', y=viz_df.columns[1:4], title = "Daily Forecasts Against Actual Prices")

fig.update_layout(yaxis_title = "$/kWh")
 
fig.show()


# We already saw from our metric_df output that Fluence won as the better forecast. The same conclusion could have easily been reached by simply looking at some visualizations. As we can see with the Differences From Actual visualization, Fluence has the least values from 0. And with subsequent visualizations, Fluence's graph is closest to the actual price graph.
