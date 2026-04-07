import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fraud Analysis Dashboard", layout="wide")

# Colours 
dark_color = "#2E2E2E"
red_main = "#E63946"
red_light = "#F28482"
red_dark = "#9D0208"
bg_color =  "white"
font_color = "#0E1117"

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_final_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# Title
st.title("Canadian Fraud Analysis Dashboard")

# ================= TOP SECTION ONLY =================
left_col, right_col = st.columns([3, 1])

with left_col:
    st.subheader("Project Summary")
    st.write("""
    This project analyzes fraud complaints in Canada to identify key trends,
    high-risk regions, and the most common fraud types. The goal is to provide
    insights that support fraud awareness and prevention.
    """)

with right_col:
    st.subheader("Group Members")

    team_members = [
    {"name": "Andrew Huynh", "page": "pages/Andrew_Huynh.py"},
    {"name": "Chinonso Maryjane Ezurike", "page": "pages/Chinonso_Ezurike.py"},
    {"name": "Ayoyimika Seide Ogunsanya", "page": "pages/Ayoyimika_Ogunsanya.py"},
]

    for member in team_members:
        st.page_link(member["page"], label=member["name"])

st.divider()

# Dataset info
st.subheader("Dataset Description")
st.write("""
The dataset contains fraud complaints including category, province,
loss amount, victim demographics, and submission channels. The dataset consists of 266,355 rows and 16 columns, 
representing a substantial collection of complaint records.

Colums such as Gender, Age Range, and Age Median are missing for approximately 10.3% of the entries, 
while Language and Method have slightly lower missing rates of 7.5% and 2.5% respectively.
""")
# ================= Data table =================
st.subheader("Data Table Preview")
st.dataframe(df.head(20))

st.divider()
# -=========== Simple KPI ================
st.subheader("Key Metrics")

total_cases = len(df)
total_loss = df["Loss"].sum()
top_category = df["Category"].value_counts().idxmax()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Cases", f"{total_cases:,}")
kpi2.metric("Total Loss", f"${total_loss:,.2f}")
kpi3.metric("Top Fraud Category", top_category)

# =========== Visualisation ================
red_dark = "#9D0208"

st.subheader("Loss by Province") # Visualisation for Loss by Province

loss_by_province = (
    df.groupby("Province State")["Loss"]
    .sum()
    .reset_index()
)

fig_bar = px.bar(
    loss_by_province,
    x="Province State",
    y="Loss",
    color_discrete_sequence=[red_dark]
)

st.plotly_chart(fig_bar, use_container_width=True)

# Visualisation for Fraud Complaints Over Time
st.subheader("Fraud Complaints Over Time")

trend = (
    df.groupby(df["Date"].dt.to_period("M"))
    .size()
    .reset_index(name="Complaint Count")
)

trend["Date"] = trend["Date"].astype(str)

fig_line = px.line(
    trend,
    x="Date",
    y="Complaint Count",
    color_discrete_sequence=[red_dark]
)

st.plotly_chart(fig_line, use_container_width=True)


# ================= Insights =================
st.divider()

st.subheader("Analytical Summary")

st.write("""
This analysis highlights distinct patterns in fraud activity across Canada, with clear
differences in both occurrence and financial impact. Identity-related fraud emerges as
one of the most frequent categories although it has low finacial loss per victim, while some less common fraud types like Spearfishing 
result in higher financial loss per victim.

Geographical trends indicate that provinces such as Ontario contributes a
significant share of total losses, suggesting concentrated areas of fraud activity.

A slight downward trend was observed in fraud complaints over time, which may indicate possible improvements in fraud awareness,
preventive measures, or reporting behavior, although periodic spikes still occur.

These insights emphasize the need for targeted fraud prevention strategies, improved
public awareness, and continuous monitoring to reduce financial losses and protect
vulnerable groups.
""")