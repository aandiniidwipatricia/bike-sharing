import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset dari file CSV
day_df = pd.read_csv('dashborad/day_clean.csv')

# Sidebar
st.sidebar.title("Bike Rental Analysis")
st.sidebar.write("Choose the analysis to display:")

# Menjumlahkan semua elemen dalam kolom casual dan registered
total_casual = sum(day_df['casual'])
total_registered = sum(day_df['registered'])

# Membuat data untuk pie plot
data = [total_casual, total_registered]
labels = ['Casual', 'Registered']

# Bagian Pie Chart
if st.sidebar.checkbox('Show Pie Chart: Casual vs Registered'):
    st.subheader('Proportion of Casual vs Registered Users')
    
    # Membuat pie plot
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#72BCD4"])
    st.pyplot(fig)

# Mengelompokkan data berdasarkan bulan dan menjumlahkan penggunaan registered dan casual
month_usage = day_df.groupby('month', observed=False)[['registered', 'casual']].sum().reset_index()

# Menggabungkan kolom registered dan casual menjadi satu kolom
month_usage['total_usage'] = month_usage['registered'] + month_usage['casual']

fig, ax = plt.subplots(figsize=(10, 6))

# Bagian Barplot Penggunaan Sepeda per Bulan
if st.sidebar.checkbox('Show Bar Plot: Monthly Usage'):
    st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Bulan')
    
    fig, ax = plt.subplots(figsize=(10, 6))
  # Membuat barplot dengan data penggunaan total (gabungan registered dan casual)
plt.bar(
    month_usage['month'],
    month_usage['total_usage'],
    color='tab:blue'  # Warna untuk total penggunaan
)

# Menambahkan label dan judul pada plot
plt.xlabel('Bulan', fontsize=12)
plt.ylabel('Jumlah Penggunaan', fontsize=12)
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Bulan', fontsize=14)

# Menampilkan plot
plt.tight_layout()
plt.show()

# Barplot Berdasarkan Kondisi Cuaca
if st.sidebar.checkbox('Show Bar Plot: Usage by Weather Condition'):
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')

    plt.figure(figsize=(10,6))
sns.barplot(
    x='weather_cond',
    y='count',
    data=day_df)

plt.title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca',fontsize=12)
plt.ylabel('Jumlah Pengguna Sepeda',fontsize=12)
plt.show()

# Menambahkan informasi footer
st.sidebar.write("---")
st.sidebar.write("Dashboard created by [Andini Dwipatricia].")
