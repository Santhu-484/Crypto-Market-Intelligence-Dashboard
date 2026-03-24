import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Set page layout
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="crypto_dashboard")

# Title
st.title("🚀 Real-Time Crypto Analytics Dashboard")
st.write("Live crypto tracking using API, Python, SQL & Streamlit")

# Load data
@st.cache_data(ttl=5)
def load_data():
    df = pd.read_csv("data/crypto_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df = load_data()

# Sidebar: Coin selection
st.sidebar.header("Filter")
selected_coin = st.sidebar.selectbox("Select Coin", df["coin"].unique())

filtered_df = df[df["coin"] == selected_coin]

# Latest values for KPI cards
latest = filtered_df.sort_values("timestamp").tail(1)
col1, col2, col3 = st.columns(3)
col1.metric("💰 Price", f"${latest['price'].values[0]:,.2f}")
col2.metric("🏦 Market Cap", f"${latest['market_cap'].values[0]:,.0f}")
col3.metric("📊 Volume", f"{latest['volume'].values[0]:,.0f}")

# Price Trend (Bitcoin & Ethereum comparison)
st.subheader("📈 Price Trend (BTC vs ETH)")

btc_df = df[df["coin"] == "bitcoin"].sort_values("timestamp")
eth_df = df[df["coin"] == "ethereum"].sort_values("timestamp")

col4, col5 = st.columns(2)

with col4:
    st.write("**Bitcoin Price Trend**")
    st.line_chart(btc_df.set_index("timestamp")["price"])

with col5:
    st.write("**Ethereum Price Trend**")
    st.line_chart(eth_df.set_index("timestamp")["price"])

# Volume Trend
st.subheader("📊 Volume Trend")
with col4:
    st.write("**Bitcoin Volume Trend**")
    st.line_chart(btc_df.set_index("timestamp")["volume"])

with col5:
    st.write("**Ethereum Volume Trend**")
    st.line_chart(eth_df.set_index("timestamp")["volume"])

# Latest Data Table
st.subheader("📋 Latest Data")
st.dataframe(filtered_df.tail(10))