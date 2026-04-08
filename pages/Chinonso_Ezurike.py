import streamlit as st
import pandas as pd
import calendar

st.set_page_config(page_title="Maryjane's Profile", layout="wide")

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_final_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()
victims_df = df[df["Complaint Type"] == "Victim"].copy()

# ================= HEADER =================
st.title("Chinonso Maryjane Ezurike")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("maryjaneo1.jpg", width=180, caption="Profile Photo")

with col2:
    st.subheader("Role")
    st.write("Data Analysis Lead")

    st.subheader("Project Contribution")
    st.write("""
    Chinonso Maryjane Ezurike contributed to the data preparation and analytical
    aspect of the project. She is responsible for transforming raw data into 
    meaningful insights that support informed decision-making. She explores 
    and analyzes datasets to identify patterns, trends, and relationships.
    """)

st.divider()

# ================= ANALYTICS SECTION =================
st.header("Analytical Outputs")

# 1. Most Affected Age Groups
st.subheader("1. Most Affected Age Groups")
st.markdown("**Metric used:** Victim frequency by `Age Range`")
age_counts = victims_df["Age Range"].value_counts().reset_index()
age_counts.columns = ["Age Range", "Count"]
st.dataframe(age_counts, use_container_width=True)

# 2. Most Affected Gender Groups
st.subheader("2. Most Affected Gender Groups")
st.markdown("**Metric used:** Victim frequency by `Gender`")
gender_counts = victims_df["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]
st.dataframe(gender_counts, use_container_width=True)

# 3. Top Provinces by Loss
st.subheader("3. Top Provinces by Loss")
st.markdown("**Metric used:** Sum of `Loss` grouped by `Province State`")
loss_by_province = (
    df.groupby("Province State")["Loss"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
loss_by_province.columns = ["Province State", "Total Loss"]
st.dataframe(loss_by_province, use_container_width=True)

# 4. Fraud Complaints Over Time
st.subheader("4. Fraud Complaints Over Time")
st.markdown("**Metric used:** Monthly complaint count using `Date`")
trend = (
    df.groupby(df["Date"].dt.to_period("M"))
    .size()
    .reset_index(name="Complaint Count")
)
trend["Date"] = trend["Date"].astype(str)
st.dataframe(trend, use_container_width=True)

# 5. Most Damaging Fraud per Victim
st.subheader("5. Most Damaging Fraud per Victim")
st.markdown("**Metric used:** Average `Loss per Victim` by fraud `Category`")
damage_df = victims_df[victims_df["Victims"] > 0].copy()
damage_df["Loss per Victim"] = damage_df["Loss"] / damage_df["Victims"]

damage = (
    damage_df.groupby("Category")["Loss per Victim"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
st.dataframe(damage, use_container_width=True)

# 6. Months with Highest Fraud Cases
st.subheader("6. Months with Highest Fraud Cases")
st.markdown("**Metric used:** Complaint count grouped by `Month`")

monthly_spike = (
    victims_df.groupby("Month")
    .size()
    .reset_index(name="Complaint Count")
)

monthly_spike["Month Name"] = monthly_spike["Month"].apply(lambda x: calendar.month_name[int(x)] if pd.notnull(x) else "Unknown")
monthly_spike = monthly_spike.sort_values(by="Complaint Count", ascending=False).reset_index(drop=True)

st.dataframe(monthly_spike, use_container_width=True)

st.divider()

# ================= SUMMARY INSIGHTS =================
st.subheader("Analytical Summary")
st.write("""
The analysis shows that fraud patterns vary across provinces, demographic groups,
and time periods. Victim-focused metrics helped identify the most affected age
and gender groups, while regional loss analysis highlighted provinces with the
greatest financial impact. Additional analysis of loss per victim showed that
some fraud categories may be less frequent but more financially damaging.
""")