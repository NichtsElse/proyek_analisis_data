import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df


df = load_data()

st.title("🚲 Advanced Bike Sharing Dashboard")

# ================= KPI =================
col1, col2, col3 = st.columns(3)
col1.metric("Total Rental", int(df['cnt'].sum()))
col2.metric("Average Rental", round(df['cnt'].mean(),2))
col3.metric("Peak Month", int(df.groupby('mnth')['cnt'].mean().idxmax()))

# ================= Sidebar Filter =================
st.sidebar.header("Interactive Filter")
month = st.sidebar.multiselect("Month", sorted(df['mnth'].unique()), default=sorted(df['mnth'].unique()))
workingday = st.sidebar.selectbox("Working Day", ["All","Weekday","Weekend"])

df = df[df['mnth'].isin(month)]

if workingday == "Weekday":
    df = df[df['workingday']==1]
elif workingday == "Weekend":
    df = df[df['workingday']==0]


st.subheader("📊 Monthly Seasonality")
fig1, ax1 = plt.subplots()
df.groupby('mnth')['cnt'].mean().plot(marker='o', ax=ax1)
st.pyplot(fig1)

df['temp_cat'] = pd.cut(df['temp'], bins=3, labels=['Dingin','Sedang','Panas'])
df['hum_cat'] = pd.cut(df['hum'], bins=3, labels=['Rendah','Sedang','Tinggi'])
df['wind_cat'] = pd.cut(df['windspeed'], bins=3, labels=['Lambat','Sedang','Kencang'])


tab1, tab2, tab3 = st.tabs(["Suhu","Kelembapan","Kecepatan Angin"])

with tab1:
    fig3, ax3 = plt.subplots()
    df.groupby('temp_cat')['cnt'].mean().plot(kind='bar', ax=ax3)
    st.pyplot(fig3)
    st.write("""
    ### Analisis dampak suhu pada pengendara sepeda:
    rata-rata penyewaan sepeda meningkat seiring kenaikan suhu. Penyewaan 
    terendah terjadi pada suhu dingin, meningkat pada suhu sedang, dan 
    mencapai puncaknya pada suhu panas. Hal ini mengindikasikan bahwa kondisi 
    suhu yang lebih hangat mendorong aktivitas bersepeda karena lebih nyaman bagi pengguna.
    """)
    
with tab2:
    fig4, ax4 = plt.subplots()
    df.groupby('hum_cat')['cnt'].mean().plot(kind='bar', ax=ax4)
    st.pyplot(fig4)
    st.write("""
    ### Analisis dampak Kelembapan pada pengendara sepeda:
    rata-rata penyewaan sepeda menurun seiring meningkatnya kelembapan. 
    Penyewaan tertinggi terjadi pada kelembapan rendah, menurun pada 
    kelembapan sedang, dan terendah pada kelembapan tinggi. Hal ini 
    mengindikasikan bahwa kelembapan yang tinggi dapat menurunkan 
    kenyamanan bersepeda sehingga berdampak pada penurunan permintaan.
    """)
    
with tab3:
    fig5, ax5 = plt.subplots()
    df.groupby('wind_cat')['cnt'].mean().plot(kind='bar', ax=ax5)
    st.pyplot(fig5)
    st.write("""
    ### Analisis dampak Kecepatan Angin pada pengendara sepeda:
    rata-rata penyewaan sepeda tertinggi terjadi pada kecepatan angin 
    sedang, diikuti angin lambat, sedangkan angin kencang memiliki jumlah 
    penyewaan terendah. Hal ini mengindikasikan bahwa kondisi angin yang
     terlalu kuat dapat menurunkan kenyamanan bersepeda sehingga berdampak
     pada penurunan permintaan, sementara angin sedang menciptakan kondisi 
    yang lebih optimal untuk aktivitas bersepeda.
    """)

st.subheader("📌 Insight Utama")

st.write("""
- Penyewaan sepeda menunjukkan pola musiman dengan puncak pada pertengahan tahun
- Suhu lebih hangat meningkatkan penyewaan
- Kelembapan tinggi menurunkan permintaan
- Angin sedang menghasilkan permintaan tertinggi
""")
