import streamlit as st
from datetime import timedelta
import pandas as pd
import plotly.express as px

st.title('Labor prediction')

se = pd.read_csv("gestation_weeks.txt", header=None)[0]


counts = se.value_counts(normalize=True, sort=False).to_frame(name="Ratio")

due_date = st.date_input("Due date")
conception_date = due_date - timedelta(weeks=40)
counts["weeks"] = counts.index
counts = counts[counts['weeks'].between(30 ,45)]
counts["Date"] = counts['weeks'].apply(lambda w: conception_date+timedelta(weeks=w))

fig = px.line(counts, x="Date", y="Ratio")
fig.add_vline(x=due_date, line_width=3, line_dash="dash", line_color="green")
st.plotly_chart(fig)
