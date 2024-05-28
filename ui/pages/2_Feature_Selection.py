import streamlit as st
import pandas as pd
import pymongo
import json
import os

# MongoDB connection setup
def init_connection():
    try:
        connection_string = st.secrets["mongo"]["connection_string"]
        client = pymongo.MongoClient(connection_string)
        client.admin.command('ping')  # Ping to check connection
        return client
    except pymongo.errors.ConnectionFailure as ce:
        st.error(f"MongoDB connection failed: {ce}")
        raise
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        raise ConnectionError("Failed to connect to MongoDB")

client = init_connection()

# Fetch data from MongoDB
@st.cache_data
def fetch_data():
    db_name = "bitcoinprice"  # Adjust as necessary
    collection_name = "Dataset_Raw"  # The collection name you specified
    db = client[db_name]
    collection = db[collection_name]
    data = list(collection.find({}))
    return pd.DataFrame(data)

# Set directories
ROOT_DIR = "/Users/leochoizero/Desktop/code_files/MSBD5003_project_UI"
FEATURES_DIR = ROOT_DIR + "/features"

# Features paths
FEATURES_CORRELATION = FEATURES_DIR + "/features_correlation.json"
BASE_FEATURES = FEATURES_DIR + "/base_features.json"
BASE_AND_MOST_CORR_FEATURES = FEATURES_DIR + "/base_and_most_corr_features.json"
BASE_AND_LEAST_CORR_FEATURES = FEATURES_DIR + "/base_and_least_corr_features.json"

# Load features from JSON
def load_features(path):
    with open(path, 'r') as file:
        return json.load(file)

st.set_page_config(layout="wide", page_title="Feature Selection", page_icon="📈")
st.markdown(
    """
    <style>
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .data-card {
            border: 1px solid #52546a;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 10px grey;
            background-color: #f6f6f6;
            color: #333;
            font-family: 'Space Grotesk', sans-serif;
        }
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

# Load data
df = fetch_data()
if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['market-price'] = df['market-price'].astype(float)

st.title("Feature Selection")
st.subheader("Base Features")
st.write(load_features(BASE_FEATURES))
st.subheader("Base and Most Correlated Features")
st.write(load_features(BASE_AND_MOST_CORR_FEATURES))
st.subheader("Base and Least Correlated Features")
st.write(load_features(BASE_AND_LEAST_CORR_FEATURES))
