import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("births.csv")
df = df[df['gestation_weeks'].between(30 ,45)]  # Filter out outliers
percentage_inductions = df["induction"].value_counts(normalize=True)["Y"]
today = datetime.today()

st.header('🐣 Labor prediction: when will I deliver? 🤷‍♀️')
st.markdown("""Please enter your due date and we'll show you the likelihood of delivery 
               around the due date.""")
due_date = st.date_input(
    "Due date (40 weeks after your last period)",
    today + relativedelta(months=1)
)

n_previous_children = st.selectbox(
    "Number of previous children", ["Include all", 0, 1, 2, "3 or more"]
)

if n_previous_children != "Include all":
    if n_previous_children == "3 or more":
        df = df[df["n_previous_children"] > 2]
    else:
        df = df[df["n_previous_children"] == n_previous_children]

induction = st.checkbox(
    f"Include inductions? ({percentage_inductions:.1%} of all deliveries)", value=False
)

if not induction:
    df = df[df["induction"] == "N"]


st.markdown(f"Number of included deliveries in the U.S. in 2019: {len(df):,}.")

se = df["gestation_weeks"]
counts = se.value_counts(normalize=True, sort=False).to_frame(name="Ratio")
conception_date = due_date - timedelta(weeks=39)
counts["weeks"] = counts.index
counts["Date"] = counts['weeks'].apply(lambda w: conception_date+timedelta(weeks=w))
counts.set_index(pd.DatetimeIndex(counts['Date']), inplace=True)
counts = counts['Ratio'].resample('D').mean()
interpolated_ratios = (counts.interpolate('pchip', order=5) / 7).to_frame(name="PDF")
interpolated_ratios = interpolated_ratios[
    interpolated_ratios.index > today + relativedelta(days=1)
]
interpolated_ratios = interpolated_ratios/(interpolated_ratios.sum())
interpolated_ratios.loc[today] = 0.
interpolated_ratios.sort_index(inplace=True)
interpolated_ratios["CDF"] = interpolated_ratios["PDF"].cumsum()

# Plots
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=interpolated_ratios.index, y=interpolated_ratios["PDF"], line_shape='spline', name="Proba"),
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

fig.update_xaxes(**{
    "range": [today, due_date + timedelta(weeks=4)],    
})
# Uncomment to add a line for the current day
# fig.add_vline(
#     x=today, line_width=2, line_dash="dash", line_color="orange", name="Today"
# )
# fig.add_annotation(x=today, y=1.05*interpolated_ratios["PDF"].max(),
#                    text="Today", showarrow=False, xshift=-35, font=dict(color="orange"))

fig.add_vline(
    x=due_date, line_width=2, line_dash="dash", line_color="green", name="Due date"
)
fig.add_annotation(x=due_date, y=1.05*interpolated_ratios["PDF"].max(),
                   text="Due date", showarrow=False, xshift=-35, 
                   font=dict(color="green"))
fig.update_xaxes({"title": "Date"})
fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '''The data takes into account all births in the US in 2019 and is provided by the 
    [Center for Disease Control and Prevention](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm). 
    The code and preprocessing can be found [here](https://github.com/nkthiebaut/labor-prediction/blob/main/streamlit_app.py).''' 
) 
