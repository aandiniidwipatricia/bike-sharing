import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("dashboard/day_clean.csv")  

# Sidebar untuk pemilihan filter
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=['All'] + list(day_df['year'].unique()))
selected_month = st.sidebar.selectbox("Pilih Bulan", options=['All'] + list(day_df['month'].unique()))
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca", options=['All'] + list(day_df['weather_cond'].unique()))

# Filter data berdasarkan input dari sidebar
filtered_data = day_df.copy()

# Terapkan filter hanya jika opsi selain "All" dipilih
if selected_year != 'All':
    filtered_data = filtered_data[filtered_data['year'] == selected_year]

if selected_month != 'All':
    filtered_data = filtered_data[filtered_data['month'] == selected_month]

if selected_weather != 'All':
    filtered_data = filtered_data[filtered_data['weather_condition'] == selected_weather]

# Tampilan di halaman utama
st.title('Bike Rentals Dashboard')
st.write(f"Menampilkan data untuk Tahun {selected_year}, Bulan {selected_month}, dan Cuaca {selected_weather}")

# Rangkuman statistik data yang difilter
st.header("Rangkuman Statistik")
st.write(filtered_data.describe(include='all'))

# Visualisasi distribusi jumlah penyewaan berdasarkan hari kerja dan hari libur
st.header("Distribusi Penyewaan Sepeda: Hari Kerja vs Hari Libur")
comparison_df = filtered_data.groupby('workingday').agg({
    'count': ['sum', 'mean']
}).reset_index()

# Membuat bar chart untuk total dan rata-rata penyewaan
fig, ax = plt.subplots(figsize=(8, 6))

# Bar chart total sewa
colors = sns.color_palette('Set2', 2)
ax.bar(comparison_df['workingday'].map({0: 'Hari Kerja', 1: 'Hari Libur'}), comparison_df['count']['sum'], color=colors)
ax.set_title('Total Penyewaan Sepeda: Hari Kerja vs Hari Libur')
ax.set_xlabel('Tipe Hari')
ax.set_ylabel('Total Penyewaan')

# Menambahkan angka di atas bar
for i, v in enumerate(comparison_df['count']['sum']):
    ax.text(i, v + 500, format(int(v), ','), ha='center')

st.pyplot(fig)

# Visualisasi distribusi penyewaan berdasarkan cuaca
st.header("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")
weather_df = filtered_data.groupby('weather_cond').agg({
    'count': 'sum'
}).reset_index()

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(weather_df['weather_cond'], weather_df['count'], color=sns.color_palette("Set2", len(weather_df)))
ax.set_title('Total Penyewaan Berdasarkan Kondisi Cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Total Penyewaan')

# Menambahkan angka di atas bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 500, format(int(yval), ','),
            ha='center', va='bottom')

st.pyplot(fig)

# Visualisasi distribusi pengguna casual dan registered per tahun
st.header("Total Penyewaan Pengguna Casual dan Registered per Tahun")
yearly_counts = filtered_data.groupby('year').agg({
    'casual': 'sum',
    'registered': 'sum'
}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
x = range(len(yearly_counts))

# Plot batang untuk 'casual' dan 'registered'
ax.bar(x, yearly_counts['casual'], width=bar_width, color='skyblue', label='Casual')
ax.bar([p + bar_width for p in x], yearly_counts['registered'], width=bar_width, color='lightgreen', label='Registered')

# Tambahkan label dan judul
ax.set_xlabel('Tahun')
ax.set_ylabel('Total Penyewaan')
ax.set_title('Total Penyewaan Casual dan Registered per Tahun')
ax.set_xticks([p + bar_width / 2 for p in x])
ax.set_xticklabels(yearly_counts['year'])

ax.legend()
st.pyplot(fig)
