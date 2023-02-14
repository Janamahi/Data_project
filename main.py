# Imports required ---
import streamlit as st
import sqlite3 as sqlite
import pandas as pd

## Instructions:
#Go in shell
#write "pip install--upgrade streamlit"
#launch with "streamlit run main.py"


@st.cache_data
def get_data():
  con = sqlite.connect("Fake_sales_data.db")
  data = pd.read_sql_query("SELECT * from SalesA", con)
  return data


data = get_data()

st.title('Welcome to the Streamlit Tour! 🎈')
with st.expander("About this App"):
  st.write("""
         This app will introduce you to the Streamlit Library which
         helps to build and deploy data driven web apps with ease using Python. 😉
     """)
st.title('Sales Dashboard')

st.write(f"we have {len(data)} datapoints")

#1. select company and sum of the sales
choice = st.selectbox("Select a company", data["company"].unique(), index=0)

new_data = data[data["company"] == choice]
st.write(new_data.head())
st.write(f"Sum of sales {choice}:")
st.write(new_data["price"].sum())

#A way to select demographic based data
ppl = st.selectbox("Select a category", new_data["cat"].unique(), index=0)
new_data = new_data[new_data["cat"] == ppl]
st.write(ppl)

#Multiple selection of the category
#ppl = st.multiselect("Select a category", ['Young','Active','Retired'])
#new_data = new_data[['Young','Active','Retired'] == ppl]
#st.write(ppl)

#print the sum of price per week
st.write(f"Sum of sales on weekly basis {choice}:")
perweek = new_data.groupby("week")["price"].sum()
st.write(perweek)

#plot the sales through time
st.write(f"Plot of sales by time {choice}:")
st.line_chart(perweek, y="price")
#st.write(data)