import streamlit as st
import pandas as pd
import plotly.express as px

# Set directories
ROOT_DIR = "/Users/leochoizero/Desktop/code_files/MSBD5003_project_UI"
DATASET_RAW_DIR = ROOT_DIR + "/datasets/raw"
DATASET_NAME = "bitcoin_blockchain_data_15min_formatted"
DATASET_RAW = DATASET_RAW_DIR + "/" + DATASET_NAME + ".parquet"


# Load dataset
@st.cache_data
def load_dataset():
    df = pd.read_parquet(DATASET_RAW)
    # Example of specifying a path that should be writable
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['market-price'] = df['market-price'].astype(float)
    return df

# Helper function to format numbers as K, M, B, etc.
def human_format(num):
    num = float(num)
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f'${num:.1f}{" KMGTPE"[magnitude]}'

# Streamlit page configuration
st.set_page_config(layout="wide", page_title="Bitcoin Data Dashboard", page_icon="📈")

# Load data
df = load_dataset()


import pandas as pd

# # Load Parquet file
# df = pd.read_parquet('/Users/leochoizero/Desktop/code_files/MSBD5003_project_UI/datasets/raw/bitcoin_blockchain_data_15min_formatted.parquet')

# # Convert timestamps to a string in an unambiguous format
# df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# # Save to JSON
# df.to_json('/Users/leochoizero/Desktop/code_files/MSBD5003_project_UI/datasets/raw/bitcoin_blockchain_data_15min_formatted.json', orient='records', lines=True)



# Apply custom CSS
st.markdown(
    """
    <style>
        footer {visibility: hidden;}
        header {visibility: hidden;}
        /* Custom CSS for cards */
        .data-card {
            border: 1px solid #52546a;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 10px grey;
            background-color: #f6f6f6;
            color: #333;
            font-family: 'Space Grotesk', sans-serif;
        }
        /* Typography */
        .price-details {
            font-size: 24px; 
            font-weight: bold;
            color: #333;
        }
        .title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True
)

# Filtering UI
year_month = st.selectbox("Select Year and Month", options=pd.to_datetime(df['timestamp']).dt.to_period("M").unique().astype(str))
filtered_df = df[df['timestamp'].dt.to_period('M') == year_month]

# Column layout
col_chart, col_data = st.columns([3, 1])  # Proportion of 3:1 for chart to data cards

with col_chart:
    st.header("Monthly Bitcoin Market Price Chart")
    # Creating an interactive line chart for market-price using Plotly
    fig = px.line(filtered_df, x='timestamp', y='market-price', labels={'timestamp': 'Timestamp', 'market-price': 'Market Price'}, title='Market Price of Bitcoin Over Time')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

with col_data:
    st.header("Market Details")
    # Highest Price Card
    st.markdown(f"<div class='data-card'><span class='title'>Highest Price:</span><br><span class='price-details'>{human_format(filtered_df['market-price'].max())}</span></div>", unsafe_allow_html=True)
    # Lowest Price Card
    st.markdown(f"<div class='data-card'><span class='title'>Lowest Price:</span><br><span class='price-details'>{human_format(filtered_df['market-price'].min())}</span></div>", unsafe_allow_html=True)
    # Trade Volume Card
    st.markdown(f"<div class='data-card'><span class='title'>Trade Volume USD:</span><br><span class='price-details'>{human_format(filtered_df['trade-volume-usd'].sum())}</span></div>", unsafe_allow_html=True)
    # Number of Transactions Card
    st.markdown(f"<div class='data-card'><span class='title'>Number of Transactions:</span><br><span class='price-details'>{filtered_df['n-transactions'].sum()}</span></div>", unsafe_allow_html=True)


# with col_chart:
st.header("Yearly Bitcoin Market Price Chart")
# Creating an interactive line chart for market-price using Plotly
fig = px.line(df, x='timestamp', y='market-price', labels={'timestamp': 'Timestamp', 'market-price': 'Market Price'}, title='Market Price of Bitcoin Over Time')
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig, use_container_width=True)

# with col_data:
st.header("Traning & Validation Data Details")
st.write(df.describe())  # Displays a summary table with statistical info like mean, std, etc.

# # Optional: Additional interactivity or information about the dataset
# with st.expander("More Information"):
#     st.write("Here you can provide more insights or download links for the dataset.")

