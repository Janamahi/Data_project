#Imports required ---
import streamlit as st
import sqlite3 as sqlite
import pandas as pd
#import altair as alt
import plotly.express as px

## Instructions:
# Go in Shell (on the right)
# write "pip install --upgrade streamlit"
# launch with "streamlit run main.py"


@st.cache_data
# Fetching data
def get_data():
  con = sqlite.connect("Fake_sales_data.db")
  data = pd.read_sql_query("SELECT * from  SalesA", con)
  return data


data = get_data()
data['company'] = data['company'].astype('string')
data['cat'] = data['cat'].astype('string')

st.title('Welcome to the Streamlit Tour! 🎈')
with st.expander("About this App"):
  st.write("""
   This app will introduce you to the Streamlit Library which
   helps to build and deploy data driven web apps with ease using Python. 😉
   """)

st.title('Sales Dashboard')
st.write("Analyisng the sales data of companies in SalesA dataset")
st.write(f"We have {len(data)} datapoints")

# Selection of Company and sum of total sales
company = st.selectbox("Select a Company", data["company"].unique(), index=0)

new_data = data[data["company"] == company]
st.write(f"Total sum of sales for {company}:")
st.write(new_data["price"].sum())

# Category selection
category = st.multiselect("Select a Category",
                          data["cat"].unique(),
                          default="Young")

# Data filtering
data_selection = data.query("company == @company & cat == @category")

# 1. Differnt for Products Sold data and chart
st.write(f"Products Sold for {company} of {category} category:")

st.write(f"We have {len(data_selection)} datapoints")

st.write(" Category and price range of different products:")
prod_sold = data_selection[['cat', 'price']].value_counts().reset_index()
st.write(prod_sold.groupby(["cat"])["price"].unique())
st.write(prod_sold.head())

#Visualisation
prod_sold.columns = [*prod_sold.columns[:-1], 'count']

plot_bar = px.bar(
  prod_sold,
  x='price',
  y='count',
  color='cat',
  title='<b> Analysis of different products sold using bar chart </b>')

st.plotly_chart(plot_bar)

# Volume of Sales

st.write(f"Volume of Sales for {company} in {category} category :")
volume_sales = data_selection["price"].count()
st.write(volume_sales)

# Revenue

st.write(f"Revenue for {company} in {category} category :")
data_selection['price'] = data['price'].astype('float')
revenue = data_selection["price"].sum()
st.write(revenue)

# Volume of sales per week
volume_per_week = data_selection.groupby(["week"
                                          ])["price"].count().reset_index()

# The revenues per week
sum_per_week = data_selection.groupby(["week"])["price"].sum().reset_index()

# Plot volume & revenue through time

st.write(" Plotting Volume & Revenue through Time:")
tab1, tab2 = st.tabs(["Volume", "Revenue"])

with tab1:
  figvol = px.line(volume_per_week,
                   x="week",
                   y="price",
                   title='Volume through time')
  st.plotly_chart(figvol)

with tab2:
  figrev = px.line(sum_per_week,
                   x="week",
                   y="price",
                   title='Revenue through time')
  st.plotly_chart(figrev)
