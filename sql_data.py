import warnings
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
from PIL import Image

warnings.filterwarnings('ignore')

####### web image
image = Image.open(fp="Techno.jpeg")

st.set_page_config(page_title="Daily Report",layout='wide',page_icon=image)


############## import the datasets ###########
@st.cache_data
def extract_data():
    file_name = r"Sql_techno.xlsx"
    df = pd.read_excel(io=file_name)

    return df

dataframe = extract_data()


# Sidebar header
st.sidebar.header("*Please Filter Here*")
st.sidebar.markdown("---")
Names = st.sidebar.multiselect(
    "Select The Name",
    options=dataframe['Names'].unique(),
    default=dataframe['Names'].unique()
)


month = dataframe['Month']
Month = st.sidebar.multiselect(
    "Select The Months",
    options=dataframe['Month'].unique(),
    default=dataframe['Month'].unique()

)


dataframe = dataframe.query(
    "Names == @Names & Month == @Month  "
)

dataframe2 = dataframe[dataframe['Time'] =='5.00 PM - 6.00 PM']

#################  KPI  ####################
st.header(" :chart_with_upwards_trend: Daily Calling Data Report")
avg_time = round(dataframe2['Total Calll'].sum()/dataframe2['Day'].count(),2)
total_call = dataframe['In Between Hour Call'].sum()
day_diff = dataframe['Day'].nunique()
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Month Avg. Call's")
    st.subheader(f"{avg_time}")

with right_column:
    st.subheader("Total Call's")
    st.subheader(f"{total_call}")

with middle_column:
    st.subheader("Report Day's")
    st.subheader(f'{day_diff}')

st.markdown("---")


#################### plots #####################

dataframe2 = dataframe[dataframe['Time'] =='5.00 PM - 6.00 PM']
fig = plt.figure(figsize=(18,7))
ax = fig.add_subplot()
sns.lineplot(data=dataframe2,x ="Date",y = "Total Calll",ci =13,hue=dataframe.Names,markers="o",style=True,linewidth=3,markersize=12).set_title(label=("Total Call Each Days"),fontsize=17)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
ax.xaxis.set_major_locator(mdates.DayLocator())
sns.despine(right=True,top=True)
plt.tick_params(axis='x',rotation=45,size=16)
plt.tick_params(axis='y',size=15)
plt.xlabel(None)
plt.ylabel("Total Call",size=15)
plt.grid(axis='y')
plt.legend(loc='upper right',fontsize=10)
st.pyplot(fig)
st.markdown("- -")

###  Dataframe
st.subheader("DataFrame")
dataframe['Date'] = dataframe['Date'].dt.date
st.dataframe(dataframe,use_container_width=True)



watermark = """
<style>
#mainmenu {visibility :hidden;}
footer {visibility :hidden;}
</style>
"""
st.markdown(watermark,unsafe_allow_html=True)
