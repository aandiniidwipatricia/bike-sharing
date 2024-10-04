import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv("dashboard/day_clean.csv")

# Mengubah nama kolom
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

# Sidebar untuk memilih opsi analisis
st.sidebar.header("Pilih Opsi Analisis")

# Pilihan visualisasi
options = st.sidebar.selectbox(
    "Pilih visualisasi:",
    ("Jumlah Penyewaan per Bulan", "Penyewaan Berdasarkan Musim", "Penyewaan Berdasarkan Hari dalam Minggu")
)

# Fungsi untuk menampilkan jumlah penyewaan per bulan
def monthly_rentals():
    monthly_rent_df = day_df.groupby('month')['count'].sum().reindex(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        fill_value=0
    )
    
    # Menampilkan data bulanan
    st.write("Data Bulanan:", monthly_rent_df)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_rent_df.index, y=monthly_rent_df.values, color='blue')  # Menggunakan warna tetap
    plt.title("Jumlah Penyewaan Sepeda per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)

# Fungsi untuk menampilkan penyewaan berdasarkan musim
def season_rentals():
    season_rent_df = day_df.groupby('season')['count'].sum().reset_index()
    
    # Menampilkan data per musim
    st.write("Data Musiman:", season_rent_df)

    plt.figure(figsize=(10, 5))
    sns.barplot(x='season', y='count', data=season_rent_df, color='blue')  # Menggunakan warna tetap
    plt.title("Jumlah Penyewaan Sepeda per Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)

# Fungsi untuk menampilkan penyewaan berdasarkan hari dalam minggu
def weekday_rentals():
    weekday_rent_df = day_df.groupby('weekday')['count'].sum().reset_index()
    
    # Menampilkan data per hari
    st.write("Data Hari dalam Minggu:", weekday_rent_df)

    plt.figure(figsize=(10, 5))
    sns.barplot(x='weekday', y='count', data=weekday_rent_df, color='blue')  # Menggunakan warna tetap
    plt.title("Jumlah Penyewaan Sepeda per Hari dalam Minggu")
    plt.xlabel("Hari dalam Minggu")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)

# Menampilkan visualisasi berdasarkan pilihan
if options == "Jumlah Penyewaan per Bulan":
    monthly_rentals()
elif options == "Penyewaan Berdasarkan Musim":
    season_rentals()
elif options == "Penyewaan Berdasarkan Hari dalam Minggu":
    weekday_rentals()

# Menampilkan informasi data
st.sidebar.subheader("Informasi Data")
st.sidebar.write(day_df.describe())
