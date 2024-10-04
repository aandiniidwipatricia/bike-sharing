import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv("dashboard/day.csv")

# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed']
day_df.drop(columns=drop_col, inplace=True)

# Mengubah nama judul kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
month_map = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
season_map = {
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
}
weekday_map = {
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
}
weather_map = {
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
}

day_df['month'] = day_df['month'].map(month_map)
day_df['season'] = day_df['season'].map(season_map)
day_df['weekday'] = day_df['weekday'].map(weekday_map)
day_df['weather_cond'] = day_df['weather_cond'].map(weather_map)

# Menyiapkan fungsi untuk membuat DataFrame yang berbeda
def create_daily_rent_df(df):
    return df.groupby(by='dateday').agg({'count': 'sum'}).reset_index()

def create_season_rent_df(df):
    return df.groupby(by='season')[['registered', 'casual']].sum().reset_index()

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({'count': 'sum'})
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return monthly_rent_df.reindex(ordered_months, fill_value=0)

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()
 
with st.sidebar:
    st.image('your_image_url_here')  # Ganti dengan URL gambar Anda
    st.title("Rental Bike Dashboard")
    selected_season = st.selectbox("Select Season", day_df['season'].unique())
    selected_month = st.selectbox("Select Month", month_map.values())
    selected_date_range = st.date_input("Select Date Range", [min_date, max_date])

# Filter data berdasarkan pilihan pengguna
filtered_data = day_df[(day_df['season'] == selected_season) & 
                        (day_df['month'] == selected_month) &
                        (pd.to_datetime(day_df['dateday']).dt.date >= selected_date_range[0]) &
                        (pd.to_datetime(day_df['dateday']).dt.date <= selected_date_range[1])]

# Membuat dan menampilkan grafik
st.subheader("Daily Rental Count")
daily_rent_df = create_daily_rent_df(filtered_data)
plt.figure(figsize=(10, 5))
sns.lineplot(data=daily_rent_df, x='dateday', y='count')
plt.xticks(rotation=45)
plt.title('Daily Rental Count Over Time')
st.pyplot(plt)

st.subheader("Monthly Rental Count")
monthly_rent_df = create_monthly_rent_df(filtered_data)
plt.figure(figsize=(10, 5))
sns.barplot(x=monthly_rent_df.index, y='count', data=monthly_rent_df)
plt.xticks(ticks=range(len(monthly_rent_df)), labels=monthly_rent_df.index, rotation=45)
plt.title('Monthly Rental Count')
st.pyplot(plt)

st.subheader("Seasonal Rental Count")
season_rent_df = create_season_rent_df(day_df)
plt.figure(figsize=(10, 5))
sns.barplot(data=season_rent_df, x='season', y='registered', color='blue', label='Registered')
sns.barplot(data=season_rent_df, x='season', y='casual', color='orange', label='Casual')
plt.title('Seasonal Rental Count')
plt.legend()
st.pyplot(plt)


