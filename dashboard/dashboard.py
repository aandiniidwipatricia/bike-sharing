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
    ("Analisis Penyewaan", "Grafik Penyewaan")
)

# Fungsi untuk menampilkan analisis penyewaan
def rental_analysis():
    # Pertanyaan 1: Berapa persen total penyewa registered dan penyewa casual?
    total_rentals = day_df['count'].sum()
    registered_rentals = day_df['registered'].sum()
    casual_rentals = day_df['casual'].sum()

    percent_registered = (registered_rentals / total_rentals) * 100
    percent_casual = (casual_rentals / total_rentals) * 100

    st.subheader("Persentase Total Penyewa")
    st.write(f"Total Penyewa: {total_rentals}")
    st.write(f"Persentase Registered User: {percent_registered:.2f}%")
    st.write(f"Persentase Casual User: {percent_casual:.2f}%")

    # Pertanyaan 2: Pada bulan apa penyewaan sepeda paling banyak?
    monthly_rent_df = day_df.groupby('month')['count'].sum()
    max_month = monthly_rent_df.idxmax()
    max_rentals = monthly_rent_df.max()

    st.subheader("Bulan dengan Penyewaan Tertinggi")
    st.write(f"Bulan: {max_month} dengan jumlah penyewaan {max_rentals}")

    # Pertanyaan 3: Apakah cuaca berperan terhadap jumlah peminjaman sepeda?
    weather_rent_df = day_df.groupby('weather_cond')['count'].sum().reset_index()
    
    # Menampilkan pengaruh cuaca
    st.subheader("Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda")
    st.write(weather_rent_df)

    # Plot pengaruh cuaca
    plt.figure(figsize=(10, 5))
    sns.barplot(x='weather_cond', y='count', data=weather_rent_df, palette='viridis')
    plt.title("Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(plt)

# Fungsi untuk menampilkan grafik penyewaan
def rental_graphs():
    # Tambahkan fungsi grafik di sini sesuai kebutuhan
    pass

# Menampilkan analisis atau grafik berdasarkan pilihan
if options == "Analisis Penyewaan":
    rental_analysis()
elif options == "Grafik Penyewaan":
    rental_graphs()

# Menampilkan informasi data
st.sidebar.subheader("Informasi Data")
st.sidebar.write(day_df.describe())
