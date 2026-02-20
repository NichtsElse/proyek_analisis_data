import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data.csv")  

df = load_data()

st.title("🚲 Bike Sharing Dashboard")


col1, col2 = st.columns(2)
with col1:
    st.metric("Total pengendara terdaftar", int(df["registered"].sum()))
with col2:
    st.metric("Total pengendara casual", int(df["casual"].sum()))


st.sidebar.header("Interactive Filter")
workingday = st.sidebar.selectbox("Working Day", ["All", "Weekday", "Weekend"])

filtered_df = df.copy()

if workingday == "Weekday":
    filtered_df = filtered_df[filtered_df["workingday"] == 1]
elif workingday == "Weekend":
    filtered_df = filtered_df[filtered_df["workingday"] == 0]


st.subheader("📊 Monthly Seasonality")

fig1, ax1 = plt.subplots()
monthly = filtered_df.groupby("mnth")["cnt"].mean().sort_index()
monthly.plot(marker="o", ax=ax1)
ax1.set_xlabel("Month")
ax1.set_ylabel("Average Rentals")
st.pyplot(fig1)


df['temp_cat'] = pd.cut(df['temp'], bins=3, labels=['Dingin','Sedang','Panas']) df['hum_cat'] = pd.cut(df['hum'], bins=3, labels=['Rendah','Sedang','Tinggi']) df['wind_cat'] = pd.cut(df['windspeed'], bins=3, labels=['Lambat','Sedang','Kencang']) tab1, tab2, tab3 = st.tabs(["Suhu","Kelembapan","Kecepatan Angin"]) with tab1: fig3, ax3 = plt.subplots() df.groupby('temp_cat')['cnt'].mean().plot(kind='bar', ax=ax3) st.pyplot(fig3) st.write(""" ### Analisis dampak suhu pada pengendara sepeda: rata-rata penyewaan sepeda meningkat seiring kenaikan suhu. Penyewaan terendah terjadi pada suhu dingin, meningkat pada suhu sedang, dan mencapai puncaknya pada suhu panas. Hal ini mengindikasikan bahwa kondisi suhu yang lebih hangat mendorong aktivitas bersepeda karena lebih nyaman bagi pengguna. """) with tab2: fig4, ax4 = plt.subplots() df.groupby('hum_cat')['cnt'].mean().plot(kind='bar', ax=ax4) st.pyplot(fig4) st.write(""" ### Analisis dampak Kelembapan pada pengendara sepeda: rata-rata penyewaan sepeda menurun seiring meningkatnya kelembapan. Penyewaan tertinggi terjadi pada kelembapan rendah, menurun pada kelembapan sedang, dan terendah pada kelembapan tinggi. Hal ini mengindikasikan bahwa kelembapan yang tinggi dapat menurunkan kenyamanan bersepeda sehingga berdampak pada penurunan permintaan. """) with tab3: fig5, ax5 = plt.subplots() df.groupby('wind_cat')['cnt'].mean().plot(kind='bar', ax=ax5) st.pyplot(fig5) st.write(""" ### Analisis dampak Kecepatan Angin pada pengendara sepeda: rata-rata penyewaan sepeda tertinggi terjadi pada kecepatan angin sedang, diikuti angin lambat, sedangkan angin kencang memiliki jumlah penyewaan terendah. Hal ini mengindikasikan bahwa kondisi angin yang terlalu kuat dapat menurunkan kenyamanan bersepeda sehingga berdampak pada penurunan permintaan, sementara angin sedang menciptakan kondisi yang lebih optimal untuk aktivitas bersepeda. """) st.subheader("📌 Insight Utama") st.write(""" - Penyewaan sepeda menunjukkan pola musiman dengan puncak pada pertengahan tahun - Suhu lebih hangat meningkatkan penyewaan - Kelembapan tinggi menurunkan permintaan - Angin sedang menghasilkan permintaan tertinggi """)


