import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')


def load_data_analysis():
    
    all_bike_df = pd.read_csv('all_bike_df.csv')
    
    days_category = {
        1: 'Hari Liburan',
        2: 'Hari Biasa',
        3: 'Hari Kerja',
    }

    all_bike_df['days_category'] = all_bike_df['season_x'].map(days_category)
    all_bike_df.groupby('days_category')['cnt_x'].mean().reset_index().sort_values('cnt_x')
    
    datetime_columns = ["dteday"]
    for column in datetime_columns:
        if column in all_bike_df.columns:
            all_bike_df[column] = pd.to_datetime(all_bike_df[column])

    min_date = all_bike_df["dteday"].min()
    max_date = all_bike_df["dteday"].max()

    return all_bike_df, min_date, max_date

def visualization(all_bike_df):
    
    tab1, tab2 = st.tabs(["Korelasi Suhu", "Distribusi Suhu"])
    with tab1:  
        st.subheader('Hubungan Antara Suhu dan Jumlah Penyewaan Sepeda')
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=all_bike_df, x='temp_x', y='cnt_x', alpha=0.5)
        plt.title('Hubungan Antara Suhu dan Jumlah Penyewaan Sepeda')
        plt.xlabel('temperature')
        plt.ylabel('Jumlah Penyewaan Sepeda')
        plt.show()
        st.pyplot(plt)
        
    with tab2:
        st.subheader('Distribusi Suhu')
        plt.figure(figsize=(12, 6))
        sns.histplot(all_bike_df['temp_x'], bins=20, kde=True)
        plt.title('Distribusi Suhu')
        plt.xlabel('temperature')
        plt.ylabel('Frekuensi')
        plt.show()
        st.pyplot(plt)
        
    
    st.subheader('Visualisasi Data Penyewaan Sepeda Dari Waktu ke Waktu')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=all_bike_df, x=all_bike_df.index, y='cnt_x')
    plt.title('Perkembangan Penyewaan Sepeda dari waktu ke waktu')
    plt.xlabel('jangka waktu')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.show()
    st.text('Visualisasi Fluktuasi data penyewaan sepeda 2011 - 2013') 
    st.pyplot(plt)
    
    st.markdown("")
    st.subheader('Perbandingan Jumlah Penggunaan Sepeda Berdasarkan Jenis Hari')
    plot = sns.catplot(data=all_bike_df, x='days_category', y='cnt_x', kind='bar', ci=False, palette='viridis')
    plot.despine(left=True)
    plt.figure(figsize=(7, 7))
    comparison = all_bike_df['days_category'].value_counts()
    plt.pie(comparison, labels=comparison.index, autopct='%2.2f%%', startangle=90, colors=sns.color_palette('viridis', len(comparison)))
    plt.title('Perbandingan Jumlah penyewaan Sepeda Berdasarkan Jenis Hari')
    st.text('Ini merupakan visualisasi data penyewa di hari liburan,hari biasa, dan hari kerja')
    st.pyplot(plt)
    
    

def filter_data(all_bike_df, start_date, end_date):
    filter_df = all_bike_df[(all_bike_df["dteday"] >= str(start_date)) & 
                      (all_bike_df["dteday"] <= str(end_date))]
    if len(filter_df) == 0:
        st.warning('Data tidak tersedia')
        st.stop()
    return filter_df

def setup_sidebar(min_date, max_date):
    with st.sidebar:
        st.image("https://d2t1xqejof9utc.cloudfront.net/screenshots/pics/6767e76862f2cd5a4e2f0613e4f37f22/large.png")       
        st.subheader('Rental Sepeda')
        selected_dates = st.date_input(
            label='Rentang Waktu', min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        if len(selected_dates) != 2:
            raise ValueError("Mohon pilih rentang waktu yang valid!")       
        start_date, end_date = selected_dates
    return start_date, end_date

def main():
    st.header('Dashboard Analisis Data Penyewaan Sepeda')
    all_bike_df, min_date, max_date = load_data_analysis()
    start_date, end_date = setup_sidebar(min_date, max_date)
    bike_df = filter_data(all_bike_df, start_date, end_date)
    visualization(bike_df)
    
    st.caption('Copyright (c) 2024')
    
    
if __name__ == '__main__':
    main()
