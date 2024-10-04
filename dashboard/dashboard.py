import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (adjust the path as needed)
data_path = "path/to/your/bike_sharing_data.csv"  # Ganti dengan path dataset Anda
day_df = pd.read_csv('dashboard/day_clean.csv')

# Data Preprocessing
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Convert numerical values to categorical
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
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
    ("Jumlah Penyewaan per Bulan", "Penyewaan Berdasarkan Musim", "Penyewaan Berdasarkan Hari dalam Minggu")
)

# Function to display monthly rentals
def monthly_rentals():
    monthly_rent_df = day_df.groupby('month')['count'].sum().reindex(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        fill_value=0
    )
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_rent_df.index, y=monthly_rent_df.values, palette='viridis')
    plt.title("Jumlah Penyewaan Sepeda per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)  # Menampilkan grafik
    
    plt.clf()  # Membersihkan figure setelah menampilkan

# Function to display season rentals
def season_rentals():
    season_rent_df = day_df.groupby('season')['count'].sum().reset_index()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x='season', y='count', data=season_rent_df, palette='viridis')
    plt.title("Jumlah Penyewaan Sepeda per Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)  # Menampilkan grafik
    
    plt.clf()  # Membersihkan figure setelah menampilkan

# Function to display weekday rentals
def weekday_rentals():
    weekday_rent_df = day_df.groupby('weekday')['count'].sum().reset_index()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x='weekday', y='count', data=weekday_rent_df, palette='viridis')
    plt.title("Jumlah Penyewaan Sepeda per Hari dalam Minggu")
    plt.xlabel("Hari dalam Minggu")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)  # Menampilkan grafik
    
    plt.clf()  # Membersihkan figure setelah menampilkan

# Display the selected visualization
if options == "Jumlah Penyewaan per Bulan":
    monthly_rentals()
elif options == "Penyewaan Berdasarkan Musim":
    season_rentals()
elif options == "Penyewaan Berdasarkan Hari dalam Minggu":
    weekday_rentals()

# Display data information
st.sidebar.subheader("Informasi Data")
st.sidebar.write(day_df.describe())
