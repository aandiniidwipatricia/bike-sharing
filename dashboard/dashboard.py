import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset dari file CSV
day_df = pd.read_csv('dashoard/day_clean.csv')

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
month_usage = day_df.groupby('month')[['registered', 'casual']].sum().reset_index()
month_usage['total_usage'] = month_usage['registered'] + month_usage['casual']

# Bagian Barplot Penggunaan Sepeda per Bulan
if st.sidebar.checkbox('Show Bar Plot: Monthly Usage'):
    st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Bulan')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(month_usage['month'], month_usage['total_usage'], color='tab:blue')
    
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Jumlah Penggunaan', fontsize=12)
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Bulan', fontsize=14)
    
    st.pyplot(fig)

# Barplot Berdasarkan Kondisi Cuaca
if st.sidebar.checkbox('Show Bar Plot: Usage by Weather Condition'):
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weather_cond', y='count', data=day_df, ax=ax)
    
    ax.set_title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca', fontsize=14)
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Jumlah Pengguna Sepeda', fontsize=12)
    
    st.pyplot(fig)

# Menambahkan informasi footer
st.sidebar.write("---")
st.sidebar.write("Dashboard created by [Your Name].")
