

import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"cafc-open-gouv-database-2021-01-01-to-2025-09-30-extracted-2025-10-01.csv")

def clean_data():

# Data Cleaning

#Checking  Data Structure
    #print("--------------------------------\nData Types:\n--------------------------------", df.dtypes)
    #print("--------------------------------\nRows,Columns:\n--------------------------------",df.shape)
    #print("--------------------------------\nNumber of Unique Values:\n--------------------------------",df.nunique())
    #print("--------------------------------\nName of Columns:\n--------------------------------", df.columns)
    #print("--------------------------------\nData Summary:\n--------------------------------", df.info())
    #print("--------------------------------\nFirst 5 Rows:\n--------------------------------",df.head())
#This doesn't seem useful, but included if you want
    #print("--------------------------------\nSummary:\n--------------------------------", df.describe())

#Check for null values in the dataset
    print(df.isnull().sum())

total_nulls = df.isnull().sum().sum()
print((df.isnull().sum() / len(df))*100)
print("There are " + str(total_nulls) + " null values in the dataset.")

#Drop all columns containing information only in French
df= df.drop(
        [
            'Type de plainte reçue',
            'Pays',
            'Catégories thématiques sur la fraude et la cybercriminalité',
            'Méthode de sollicitation',
            'Langue de correspondance',
            'Type de plainte',
            'Province/État',
            'Genre'
        ]
        , axis='columns')

#print(df.head())

#Rename column names, removing the French and keeping the English, and also removing spaces in the column names for easier access
df.rename(columns={
        "Date Received / Date reçue": "Date",
        "Numéro d'identification / Number ID": "ID",
        "Victim Age Range / Tranche d'âge des victimes": "Age Range",
        "Number of Victims / Nombre de victimes": "Victims",
        "Dollar Loss /pertes financières": "Loss",
        "Complaint Received Type": "Submission Channel",

        "Province/State": "Province State",
        "Fraud and Cybercrime Thematic Categories":"Category",
        "Solicitation Method":"Method",
        "Language of Correspondence":"Language",
        "Complaint Type":"Complaint Type"
}, inplace=True)

#print(df.head())

#Removing "_" from the column titles
df.columns = (
    df.columns
    .str.strip()    
    .str.replace("_", " ")
    .str.title()
)


#Standardize text columns by stripping whitespace and converting to title case
text_cols = [
     "Submission Channel",
     "Country", 
     "Province State", 
     "Category", 
     "Gender",
     "Complaint Type",
     "Category",
     "Method",
     "Language"]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

#Replace "Not Available" and variations for missing values with nan
df = df.replace([
    "Not Available",
    "non disponible",
    "Non disponible",
    "'Not Available / non disponible"
], np.nan)

#Fill missing values in categorical columns with "Unknown" //DISABLED
#cols = [
#     "Submission Channel",
#     "Country", 
#     "Province_State", 
#     "Category", 
#     "Gender",
#     "Complaint_Type",
#     "Category",
#     "Method",
#     "Language",
#     "Gender", 
#     "Age_Range"
#     ]
#df[cols] = df[cols].fillna("Unknown")

#Replaces slashes with underscores for easier analysis
df = df.replace(r"[/]", "_", regex=True)

 

#Except for Date column, change dashes to underscores in selected string columns for easier analysis
cols_to_update = ["Submission Channel", "Complaint Type", "Country", "Province State", "Category", "Method", "Language"]
df[cols_to_update] = df[cols_to_update].replace("-", "_", regex=True)

#print(df.head())

#Replace "_-_" first (for age range)
df = df.replace(r"_-_", "_", regex=True)    

#Replace all underscores with spaces
df = df.replace(r"_", " ", regex=True)  

#Replace all instances of "Emergency (Jail, Accident, Hospital, Help)" with "Emergency" in the Category column for easier analysis
df['Category'] = df['Category'].replace('Emergency_(Jail,_Accident,_Hospital,_Help)', 'Emergency')

df["Category"].unique()

#drop all countries that is not Canada
df=df[df["Country"] == "Canada"]

#Drop apostrophe in  Age Range Column
df["Age_Range"] = df["Age Range"].str[1:].fillna(df["Age Range"])

#print(df["Age_Range"].head())

#Remove rows with non-age values in the Age_Range column
df = df[~df["Age Range"].str.contains(r'Deceased|Décédé|Business|Entreprise|nknown', na=False, regex=True)]

df = df[~df["Age Range"].str.contains(
    r'Deceased|Décédé|Business|Enterprise',na=False,regex=True)]


#Create a new column for the average age by applying a function to the Age Range column
def range_to_avg(val):
        if isinstance(val, str):
            nums = re.findall(r'\d+', val)  # Extract all digits
            if len(nums) == 2:
                return (float(nums[0]) + float(nums[1])) / 2
            elif len(nums) == 1:
                return float(nums[0])
        return np.nan  # Handle non-strings or errors

df['Age Median'] = df['Age Range'].apply(range_to_avg)


#Remove $ and Comma  in the Loss Column
df['Loss'] = df['Loss'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
#Convert the Loss column to floating data type/numeric, coercing errors to NaN, and then fill NaN with 0
df['Loss'] = pd.to_numeric(df['Loss']).fillna(0) 

#print(df['Loss'].dtype)
#print(df['Loss'].head())

#Remove rows with unreasonable values in the Loss column
df = df[df["Loss"] >= 0]

#Drop rows where the Date column is missing
df = df.dropna(subset=["Date"])

#Convert the Date column to datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

#print(df["Date"])

#Create a new column for the year and month of the Date Column
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
print("--------------------------------\nFirst 5 Rows:\n--------------------------------",df.head())

df.to_csv('cleaned_final_data.csv', index=False)
clean_data()

#Verifying  Data Structure
print("--------------------------------\nData Types:\n--------------------------------", df.dtypes)
print("--------------------------------\nRows,Columns:\n--------------------------------",df.shape)
print("--------------------------------\nNumber of Unique Values:\n--------------------------------",df.nunique())
print("--------------------------------\nName of Columns:\n--------------------------------", df.columns)
print("--------------------------------\nData Summary:\n--------------------------------", df.info())
print("--------------------------------\nFirst 5 Rows:\n--------------------------------",df.head())