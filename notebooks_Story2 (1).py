import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load Data

st.title("Google Play Store Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("googleplaystore.csv")

    # Clean Installs
    df['Installs'] = df['Installs'].astype(str)
    df['Installs'] = df['Installs'].str.replace(',', '')
    df['Installs'] = df['Installs'].str.replace('+', '')
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    # Clean Price
    df['Price'] = df['Price'].astype(str)
    df['Price'] = df['Price'].str.replace('$', '')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Drop missing values
    df = df.dropna(subset=['Category', 'Rating', 'Installs', 'Price'])

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove outliers
    df = df[(df['Rating'] >= 1) & (df['Rating'] <= 5)]
    df = df[df['Installs'] < df['Installs'].quantile(0.99)]
    df = df[df['Price'] < df['Price'].quantile(0.99)]

    return df

df = load_data()


# Sidebar Filters

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

app_type = st.sidebar.selectbox(
    "Select App Type",
    options=["All", "Free", "Paid"]
)

# Apply filters
filtered_df = df[df['Category'].isin(category)]

if app_type != "All":
    filtered_df = filtered_df[filtered_df['Type'] == app_type]


# Metrics

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Apps", len(filtered_df))
col2.metric("Average Rating", round(filtered_df['Rating'].mean(), 2))
col3.metric("Total Installs", int(filtered_df['Installs'].sum()))


# Top Categories by Rating

st.subheader("Top Categories by Rating")

category_rating = filtered_df.groupby('Category')['Rating'].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
category_rating.head(10).plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)


# Top Categories by Installs

st.subheader("Top Categories by Installs")

category_installs = filtered_df.groupby('Category')['Installs'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
category_installs.head(10).plot(kind='bar', ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)


# Price vs Rating

st.subheader("Price vs Rating")

fig3, ax3 = plt.subplots()
ax3.scatter(filtered_df['Price'], filtered_df['Rating'])
ax3.set_xlabel("Price")
ax3.set_ylabel("Rating")
st.pyplot(fig3)


# Free vs Paid Comparison

st.subheader("Free vs Paid Apps")

filtered_df['Type'] = filtered_df['Type'].fillna('Free')

type_data = filtered_df.groupby('Type')[['Rating', 'Installs']].mean()

fig4, ax4 = plt.subplots()
type_data.plot(kind='bar', ax=ax4)
plt.xticks(rotation=0)
st.pyplot(fig4)


# Trend Over Time

st.subheader("Installs Over Time")

filtered_df['Last Updated'] = pd.to_datetime(filtered_df['Last Updated'], errors='coerce')
filtered_df['Year'] = filtered_df['Last Updated'].dt.year

trend = filtered_df.groupby('Year')['Installs'].sum()

fig5, ax5 = plt.subplots()
trend.plot(ax=ax5)
st.pyplot(fig5)