import streamlit as st
import pandas as pd
import json
import os
import config
# Set directories



ROOT_DIR = "/Users/leochoizero/Desktop/code_files/MSBD5003_project_UI"
FEATURES_DIR = ROOT_DIR + "/features"
DATASET_RAW_DIR = ROOT_DIR + "/datasets/raw"
DATASET_NAME = "bitcoin_blockchain_data_15min_formatted"
DATASET_RAW = DATASET_RAW_DIR + "/" + DATASET_NAME + ".parquet"

# Features paths
FEATURES_CORRELATION = FEATURES_DIR + "/features_correlation.json"
BASE_FEATURES = FEATURES_DIR + "/base_features.json"
BASE_AND_MOST_CORR_FEATURES = FEATURES_DIR + "/base_and_most_corr_features.json"
BASE_AND_LEAST_CORR_FEATURES = FEATURES_DIR + "/base_and_least_corr_features.json"

# Load features from JSON
def load_features(path):
    with open(path, 'r') as file:
        return json.load(file)

# Load dataset
@st.cache_data
def load_dataset():
    return pd.read_parquet(DATASET_RAW)



st.set_page_config(layout="wide", page_title="Feature selection", page_icon="📈")
st.markdown(config.condensed_page_style, unsafe_allow_html=True)


# Load data
df = load_dataset()



st.title("Feature Selection")
st.subheader("Base Features")
st.write(load_features(BASE_FEATURES))
st.subheader("Base and Most Correlated Features")
st.write(load_features(BASE_AND_MOST_CORR_FEATURES))
st.subheader("Base and Least Correlated Features")
st.write(load_features(BASE_AND_LEAST_CORR_FEATURES))

