import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the calculated metrics CSV file
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load data
file_path = "calculated_metrics.csv"
df = load_data(file_path)

# Streamlit app layout
st.title("Metrics Dashboard")
st.sidebar.title("Filters")

# Filter options
ticker_options = df['Ticker'].unique()
selected_ticker = st.sidebar.selectbox("Select a Ticker", ticker_options)

# Filter data based on the selected ticker
filtered_df = df[df['Ticker'] == selected_ticker]

# Display data
st.write(f"### Metrics for {selected_ticker}")
st.write(filtered_df)

# Plot returns
st.write("### Returns")
fig, ax = plt.subplots()
ax.plot(filtered_df['Date'], filtered_df['Return_5d'], label="5-day Return", marker='o')
ax.plot(filtered_df['Date'], filtered_df['Return_20d'], label="20-day Return", marker='o')
ax.plot(filtered_df['Date'], filtered_df['Return_60d'], label="60-day Return", marker='o')
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Return")
ax.set_title("Returns Over Time")
st.pyplot(fig)

# Plot realized volatility
st.write("### Realized Volatility")
fig, ax = plt.subplots()
ax.plot(filtered_df['Date'], filtered_df['Realized_Volatility'], label="Realized Volatility", color='orange', marker='o')
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Volatility")
ax.set_title("Realized Volatility Over Time")
st.pyplot(fig)

# Plot Z-Score
st.write("### Z-Scores")
fig, ax = plt.subplots()
ax.plot(filtered_df['Date'], filtered_df['Z_Score'], label="Z-Score", color='green', marker='o')
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Z-Score")
ax.set_title("Z-Score Over Time")
st.pyplot(fig)
