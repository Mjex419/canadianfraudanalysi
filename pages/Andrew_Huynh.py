import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Andrew's Profile", layout="wide")

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_final_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()
victims_df = df[df["Complaint Type"] == "Victim"].copy()

# ================= HEADER =================
st.title("Andrew Huynh")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("Andrew.png", width=180, caption="Profile Photo")

with col2:
    st.subheader("Role")
    st.write("Data Cleaning & Preprocessing Specialist")

    st.subheader("Project Contribution")
    st.write("""
    Andrew contributed to the data cleaning and preprocessing phase of the project.
    He was responsible for handling missing values, encoding categorical variables, and ensuring that the dataset was in a suitable format for analysis. 
    His work laid the foundation for accurate and efficient modeling by preparing the data for subsequent stages of the project
    """)

st.divider()

# ================= Data table =================
st.subheader("Data Table Preview")
st.dataframe(df.head(30))

st.divider()

# ================= Description of the dataset =================
st.subheader("Statistical Description")
st.dataframe(df.describe())

st.write(f"Total Records: {len(df)}") 

st.write("""
This table provides a statistical summary of the dataset, including central tendencies, 
distribution spread, and frequency of values across both numerical and categorical variables.
""")

st.divider()

# ================= Insights =================
st.subheader("Statistical Insights")
st.write(f"""
The standard deviation for age and month indicates variability across both demographic and temporal dimensions. 
With an age spread of 18.61 and a monthly variation of 3.4204, 
fraud cases are widely distributed across different age groups and throughout the year, 
while still showing signs of concentration in specific periods and demographics.
""")
