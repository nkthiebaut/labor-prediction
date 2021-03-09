import streamlit as st
from datetime import timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.header('🐣 Labor prediction: when will I deliver? 🤷‍♀️')
#due_date = st.sidebar.date_input("Due date")
due_date = st.date_input("Due date: just enter your due date (40 weeks after your last period) and we'll show you the likelihood of delivery around the due date (data from the CDC, details below):")

# Data import and preprocessing
se = pd.read_csv("gestation_weeks.txt", header=None)[0]
counts = se.value_counts(normalize=True, sort=False).to_frame(name="Ratio")
conception_date = due_date - timedelta(weeks=39)
counts["weeks"] = counts.index
counts = counts[counts['weeks'].between(30 ,45)]
counts["Date"] = counts['weeks'].apply(lambda w: conception_date+timedelta(weeks=w))
counts.set_index(pd.DatetimeIndex(counts['Date']), inplace=True)
counts = counts['Ratio'].resample('D').mean()
interpolated_ratios = (counts.interpolate('pchip', order=5) / 7).to_frame(name="PDF")
interpolated_ratios["CDF"] = interpolated_ratios["PDF"].cumsum()


# Plots
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=interpolated_ratios.index, y=interpolated_ratios["PDF"], name="Proba"),
    secondary_y=False,
)
fig.update_yaxes(**{
    "title_text": "Probability of labor <b>on</b> date",  
    "tickformat": ',.1%', 
    "range": [0,1.1*interpolated_ratios["PDF"].max()],    
    "color": "blue"
}, secondary_y=False)

fig.add_trace(
    go.Scatter(x=interpolated_ratios.index, y=interpolated_ratios["CDF"], 
               fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.1)', name="Cumulative proba"),
    secondary_y=True,
)
fig.update_yaxes(**{
    "title_text": "Probability of labor <b>before</b> date",  
    "tickformat": ',.0%', 
    "range": [0, 1],    
    "color": "red"
}, secondary_y=True)
fig.add_vline(x=due_date, line_width=2, line_dash="dash", line_color="green", name="Due date")

fig.add_annotation(x=due_date, y=1.05*interpolated_ratios["PDF"].max(),
                   text="Due date", showarrow=False, xshift=-35, font=dict(color="green"))
fig.update_xaxes({"title": "Date"})
fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))

st.plotly_chart(fig, use_container_width=True)

st.markdown('The data takes into account all births in the US in 2019 and is provided by the [Center for Disease Control and Prevention](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm). After unzipping, the gestation duration in weeks is extracted from the Birth Data File with the following Bash command (it takes a couple of minutes): `cat Nat2019PublicUS.c20200506.r20200915.txt | cut -c 499,500 > gestation_weeks.txt`') 
