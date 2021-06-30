from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Whose forecast is better: Fluence or the market operators?")


st.text("")


#Grab all the data from Snowflake DWH

url = URL(

    account = st.secrets["account"],
    user = st.secrets["user"],
    password = st.secrets["password"],
    warehouse = st.secrets["warehouse"],
    database =  st.secrets["database"],
    schema = st.secrets["schema"]

    )

engine = create_engine(url)

connection = engine.connect()

query1 = 'select * from  "CASESTUDY"."CASESTUDY_MINDY"."METRIC"'
dataframe = pd.read_sql_query(query1, connection)


query2 = 'select "a"."settlement_time", "a"."actual_price", "f"."p50" as "fluence_p50", "m"."p50" as "market_p50", abs("f"."p50"-"a"."actual_price") as "f_diff_a", abs("m"."p50"-"a"."actual_price") as "m_diff_a" from "CASESTUDY"."CASESTUDY_MINDY"."actual_prices" as "a" join "CASESTUDY"."CASESTUDY_MINDY"."fluence_forecast" as "f" on ("a"."settlement_time" = "f"."settlement_time") join "CASESTUDY"."CASESTUDY_MINDY"."market_forecast" as "m" on ("a"."settlement_time" = "m"."settlement_time") '
dataframe2 = pd.read_sql_query(query2, connection)


query3 = 'select * from  "CASESTUDY"."CASESTUDY_MINDY"."MONTH_AGGREGATE"'
dataframe3 = pd.read_sql_query(query3, connection)

query4 = 'select * from  "CASESTUDY"."CASESTUDY_MINDY"."DAY_AGGREGATE"'
dataframe4 = pd.read_sql_query(query4, connection)

st.write("Below we have the metrics table. It shows the metric that was chosen to determine the best forecast (rmse) and its competing metric (mae). The lower the number, the better the forecast.")

# dataframe = pd.read_csv('metric.csv')
st.dataframe(dataframe)


st.text("")
st.text("")
st.text("")


st.write("Now, let's look at the data that the metric table was built off of: actual prices (actual_price), Fluence forecast (fluence_p50) and market operators' forecast (market_p50).")


# dataframe2 = pd.read_csv('viz_df.csv')
st.dataframe(dataframe2)


st.text("")
st.text("")
st.text("")


st.write("To understand which forecast is better, it helps to:")
st.write("1. Visualize each forecasts' difference from the actual price values (closest to 0 is best).")
st.write("2. Visually inspect how far each forecast graph is from the actual price forecast graph (graph closest to actual_price one is best).")


st.text("")


st.write("Interactivity:")
st.write("At the upper right of each graph, you'll find options to download the plot, zoom, pan, hover, autoscale, reset axes, view with toggle spike lines, and specify hover output information. Controls I find most helpful are: 'Compare data on hover' and 'Toggle Spike Lines' where appropriate. Feel free to interact with your visualizalizations!")


plotly_figure1 = px.line(dataframe2, x='settlement_time', y=dataframe2.columns[4:], title='Differences from Actual: Fluence vs Market')

plotly_figure1.update_xaxes(
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

plotly_figure1.update_layout(yaxis_title= "$/kWh")

st.plotly_chart(plotly_figure1)


st.text("")
st.text("")


plotly_figure2 = px.line(dataframe2, x='settlement_time'.lower(), y=dataframe2.columns[1:4], title = "Forecasts Against Actual Prices")

plotly_figure2.update_xaxes(
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

plotly_figure2.update_layout(yaxis_title = "$/kWh")

st.plotly_chart(plotly_figure2)


st.text("")
st.text("")


#dataframe3 = pd.read_csv('viz_df_m.csv')

plotly_figure3 = px.line(dataframe3, x='settlement_time', y=dataframe3.columns[1:4], title = "Monthly Forecasts Against Actual Prices")

plotly_figure3.update_layout(yaxis_title = "$/kWh")

st.plotly_chart(plotly_figure3)


st.text("")
st.text("")


#dataframe4 = pd.read_csv('viz_df_d.csv')

plotly_figure4 = px.line(dataframe4, x='settlement_time', y=dataframe4.columns[1:4], title = "Daily Forecasts Against Actual Prices")

plotly_figure4.update_layout(yaxis_title = "$/kWh")

st.plotly_chart(plotly_figure4)


st.text("")
st.text("")


st.write("We already saw from our metrics table that Fluence won as the better forecast. The same conclusion could have easily been reached by simply looking at some visualizations. As we can see with the Differences From Actual visualization, Fluence has the least values from 0. And with subsequent visualizations, Fluence's graph is closest to the actual price graph.")


st.text("")
st.text("")


st.write("Please send any inquiries to: mindyng8855@gmail.com")
