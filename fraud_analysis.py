import pandas as pd
import calendar

# Load dataset
df = pd.read_csv(r"C:\Users\USER\Documents\Python\Project\cleaned_final_data.csv")

# Filter victims
victims_df = df[df["Complaint Type"] == "Victim"].copy()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# 1. Total loss

total_loss = df["Loss"].sum()
print(f"Total Loss: ${total_loss:,.2f}")

# Total Loss by province from highest to lowest
loss_by_province = df.groupby("Province State")["Loss"].sum().sort_values(ascending=False)
print("\nTop 5 Provinces by Loss:")
print(loss_by_province.head())

# =========2. Common Fraud Threat from highest to lowet
counts = df["Category"].value_counts()

top_category = counts.idxmax()
top_count = counts.max()

print("\nMost Common Fraud Category:")
print(f"{top_category} → {top_count}")

loss_by_category = df.groupby("Category")["Loss"].sum().sort_values(ascending=False)    # Fraud type with the most loss of money (Highest to lowest)
print("\nFraud Types with Highest Loss:")
print(loss_by_category.head())


# ========3. Most Suspectible victim by Age

# Analyze age
age_counts = victims_df["Age Range"].value_counts()
print("\nMost Affected Age Groups:")
print(age_counts.head())


# =======4. Most Suspectible victim by Gender
gender_counts = victims_df["Gender"].value_counts().reset_index()
gender_counts.columns = ["Gender", "Count"]

print("\nMost Affected Gender Groups:")
print(gender_counts.head())


# =======5. Fraud Trend over time
trend = (
    df.groupby(df["Date"].dt.to_period("M"))
    .size()
    .reset_index(name="Complaint Count")
)
print("\nFraud Trends Over Time:")
print(trend.head())


# =====6. Most Damaging Fraud per person
damage_df = victims_df[victims_df["Victims"] > 0].copy()
damage_df["Loss per Victim"] = damage_df["Loss"] / damage_df["Victims"]

damage = (
    damage_df.groupby("Category")["Loss per Victim"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
print("\nMost Damaging Fraud per Victim:")
print(damage.head())


# =====7. Months with Fraud Spikes

monthly_spike = (
    victims_df.groupby("Month")
    .size()
    .reset_index(name="Complaint Count")
    .sort_values("Month")
)

monthly_spike["Month Name"] = monthly_spike["Month"].apply(lambda x: calendar.month_name[x])

# Sorting by Complaint Count from highest to lowest
monthly_spike = monthly_spike.sort_values(by="Complaint Count", ascending=False).reset_index(drop=True)
print("\nMonths with Highest Fraud Cases:")
print(monthly_spike.head())


