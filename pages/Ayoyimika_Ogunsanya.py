import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ayoyimika's Profile", layout="wide")

# ================= COLORS =================
dark_color = "#2E2E2E"
red_main = "#E63946"
red_light = "#F28482"
red_dark = "#9D0208"
bg_color =  "white"
font_color = "#0E1117"

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_final_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()
victims_df = df[df["Complaint Type"] == "Victim"].copy()

# ================= HEADER =================
st.title("Ayoyimika Seide Ogunsanya")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("Ayopics.jpg", width=180, caption="Profile Photo")

with col2:
    st.subheader("Role")
    st.write("Data Visualization & Insights Specialist")

    st.subheader("Project Contribution")
    st.write("""
    Ayoyimika contributed to the visualization and insight communication aspect of the project.
    Her role focused on transforming the analytical outputs into clear and engaging charts that
    support data storytelling. She worked on presenting fraud categories, victim demographics,
    and financial impact patterns in a way that makes the dashboard more intuitive and informative.
    """)

st.divider()

# ================= VISUAL 1 =================
st.subheader("Most Common Fraud Categories")

top_categories = df["Category"].value_counts().reset_index()
top_categories.columns = ["Category", "Count"]

fig1 = px.bar(
    top_categories,
    x="Category",
    y="Count",
    color_discrete_sequence=[dark_color]
)
fig1.update_layout(
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=font_color,
    xaxis_title="Fraud Category",
    yaxis_title="Count"
)
st.plotly_chart(fig1, use_container_width=True)

# ================= VISUAL 2 =================
st.subheader("Fraud Types with Highest Financial Loss")

loss_by_category = (
    df.groupby("Category")["Loss"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    loss_by_category,
    x="Category",
    y="Loss",
    color_discrete_sequence=[dark_color]
)
fig2.update_layout(
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=font_color,
    xaxis_title="Fraud Category",
    yaxis_title="Total Loss"
)
st.plotly_chart(fig2, use_container_width=True)

# ================= VISUAL 3 =================
st.subheader("Most Affected Age Groups")

age_counts = victims_df["Age Range"].value_counts().reset_index()
age_counts.columns = ["Age Range", "Count"]

fig3 = px.bar(
    age_counts,
    x="Age Range",
    y="Count",
    color="Count",
    color_continuous_scale="Reds"
)
fig3.update_layout(
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=font_color,
    xaxis_title="Age Range",
    yaxis_title="Victim Count"
)
st.plotly_chart(fig3, use_container_width=True)

# ================= VISUAL 4 =================
st.subheader("Most Affected Gender Groups")

gender_counts = victims_df["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]

fig4 = px.bar(
    gender_counts,
    x="Gender",
    y="Count",
    color="Gender",
    color_discrete_sequence=[red_main, red_light, red_dark]
)
fig4.update_layout(
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=font_color,
    xaxis_title="Gender",
    yaxis_title="Victim Count"
)
st.plotly_chart(fig4, use_container_width=True)

# ================= VISUAL 5 =================
st.subheader("Most Damaging Fraud per Victim")

damage_df = victims_df[victims_df["Victims"] > 0].copy()
damage_df["Loss per Victim"] = damage_df["Loss"] / damage_df["Victims"]

damage = (
    damage_df.groupby("Category")["Loss per Victim"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig5 = px.bar(
    damage,
    x="Category",
    y="Loss per Victim",
    color_discrete_sequence=[red_dark]
)
fig5.update_layout(
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font_color=font_color,
    xaxis_title="Fraud Category",
    yaxis_title="Average Loss per Victim"
)
st.plotly_chart(fig5, use_container_width=True)

# ================= INSIGHTS =================
st.subheader("Key Insights")
st.write("""
- Fraud categories vary significantly in both frequency and financial impact.
- Some fraud types occur often, while others are less frequent but more financially damaging.
- Victim demographics such as age and gender reveal patterns in susceptibility.
- Visualization helps communicate these patterns clearly and supports better fraud awareness.
""")


