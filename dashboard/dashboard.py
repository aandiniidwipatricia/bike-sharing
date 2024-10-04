import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
day_df = pd.read_csv("dashboard/day_clean.csv")

# Data Preprocessing
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
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

# Sidebar untuk navigasi
st.sidebar.header("Pilih Opsi Analisis")
options = st.sidebar.selectbox(
    "Pilih visualisasi:",
    ("Jumlah Penyewaan Berdasarkan Bulan", "Distribusi Penyewaan Berdasarkan Cuaca", "Persentase Pengguna Casual vs Registered")
)

# Debugging: Tampilkan 5 data teratas dan informasi dataset
st.write("Dataframe Preview:")
st.write(day_df.head())
st.write(day_df.info())

# Fungsi untuk menampilkan jumlah penyewaan berdasarkan bulan
def plot_monthly_rentals():
    month_usage = day_df.groupby('month', observed=False)[['registered', 'casual']].sum().reset_index()
    month_usage['total_usage'] = month_usage['registered'] + month_usage['casual']

    # Debugging: Lihat hasil aggregasi data
    st.write("Data Setelah Grouping Berdasarkan Bulan:")
    st.write(month_usage.head())
    
    plt.figure(figsize=(10, 6))
    plt.bar(month_usage['month'], month_usage['total_usage'], color='tab:blue')
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Jumlah Penggunaan', fontsize=12)
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Bulan', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Pastikan tata letak rapi
    st.pyplot(plt.gcf())  # Tampilkan plot dengan figure saat ini
    plt.close()

# Fungsi untuk menampilkan distribusi penyewaan berdasarkan cuaca
def plot_weather_distribution():
    weather_counts = day_df.groupby('weather_cond').agg({
        'count': 'sum'
    }).reset_index()

    # Debugging: Lihat hasil aggregasi data
    st.write("Data Setelah Grouping Berdasarkan Cuaca:")
    st.write(weather_counts.head())
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='weather_cond', y='count', data=weather_counts)
    plt.title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca', fontsize=12)
    plt.ylabel('Jumlah Pengguna Sepeda', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Pastikan tata letak rapi
    st.pyplot(plt.gcf())
    plt.close()

# Fungsi untuk menampilkan persentase pengguna casual vs registered
def plot_casual_vs_registered():
    total_casual = sum(day_df['casual'])
    total_registered = sum(day_df['registered'])
    
    # Debugging: Lihat total casual vs registered
    st.write("Total Casual:", total_casual)
    st.write("Total Registered:", total_registered)

    data = [total_casual, total_registered]
    labels = ['Casual', 'Registered']

    plt.figure(figsize=(8, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#72BCD4"])
    plt.title('Persentase Pengguna: Casual vs Registered')
    plt.tight_layout()  # Pastikan tata letak rapi
    st.pyplot(plt.gcf())
    plt.close()

# Menampilkan visualisasi berdasarkan pilihan
if options == "Jumlah Penyewaan Berdasarkan Bulan":
    plot_monthly_rentals()
elif options == "Distribusi Penyewaan Berdasarkan Cuaca":
    plot_weather_distribution()
elif options == "Persentase Pengguna Casual vs Registered":
    plot_casual_vs_registered()
