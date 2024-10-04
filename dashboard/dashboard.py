import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
day_df = pd.read_csv("dashboard/day_clean.csv")

# Preprocessing
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Convert numerical values to categorical for analysis
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Sidebar for navigation
st.sidebar.header("Pilih Opsi Analisis")
options = st.sidebar.selectbox(
    "Pilih visualisasi:",
    ("Jumlah Penyewaan Sepeda Berdasarkan Bulan", "Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
)

# Function for visualizing rentals by month
def plot_monthly_rentals():
    month_usage = day_df.groupby('month').agg({'count': 'sum'}).reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=month_usage, x='month', y='count', palette='viridis')
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

# Function for visualizing rentals by weather condition
def plot_weather_condition_rentals():
    weather_usage = day_df.groupby('weather_cond').agg({'count': 'sum'}).reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=weather_usage, x='weather_cond', y='count', palette='viridis')
    plt.title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(plt)

# Show the selected visualization
if options == "Jumlah Penyewaan Sepeda Berdasarkan Bulan":
    plot_monthly_rentals()
elif options == "Distribusi Penyewaan Berdasarkan Kondisi Cuaca":
    plot_weather_condition_rentals()
