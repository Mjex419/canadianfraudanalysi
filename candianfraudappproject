import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fraud Analysis Dashboard", layout="wide")

# Title
st.title("Canadian Fraud Analysis Dashboard")

# Project summary
st.subheader("Project Summary")
st.write("""
This project analyzes fraud complaints in Canada, identifying key trends,
high-risk regions, and the most common fraud types.
""")

# Dataset info
st.subheader("Dataset Description")
st.write("""
The dataset contains fraud complaints including category, province,
loss amount, victim demographics, and submission channels. The dataset consists of 266,355 rows and 16 columns, 
representing a substantial collection of complaint records.

Colums such as Gender, Age Range, and Age Median are missing for approximately 10.3% of the entries, 
while Language and Method have slightly lower missing rates of 7.5% and 2.5% respectively.
""")

# Load data
df = pd.read_csv(r"C:\Users\USER\Documents\Python\Project\cleaned_final_data.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Simple KPI
total_loss = df["Loss"].sum()
st.metric("Total Loss", f"${total_loss:,.2f}")

# Chart
st.subheader("Loss by Province")
loss_by_province = df.groupby("Province State")["Loss"].sum().sort_values(ascending=False)
st.bar_chart(loss_by_province)

# Sidebar for navigation info
st.sidebar.title("Team Members")
st.sidebar.write("Click a member to view their profile ➡️")