import streamlit as st
import pandas as pd
import json
import os
import config

# Assuming 'config' is a module you have that stores configurations or functions

st.set_page_config(layout="wide", page_title="Bitcoin Price Prediction", page_icon="💰")
st.markdown(config.condensed_page_style, unsafe_allow_html=True)

st.sidebar.title("MSBD5003 - Group 9")
st.image('../image/bitcoin.png',width=150,output_format="PNG")

st.title("Bitcoin Price Prediction ")
st.subheader("Background")
st.write("Bitcoin is a decentralized digital currency, often referred to as cryptocurrency.\
         In this project, we will predict the bitcoin market price (USD) and compare the predicted price trend with the real price trend given in test data.")


# section = st.sidebar.radio("Go to", ["Home", "Plot Entire Data", "Data Grid", "Forecast", "More Analysis"])

# # Content based on navigation choice
# if section == "Home":
#     st.title("Bitcoin Price Prediction Dashboard")
#     st.write("Welcome to the Bitcoin Price Prediction Dashboard. Please select a section from the sidebar.")
# elif section == "Plot Entire Data":
#     st.header("Plot Entire Data")
#     # Assuming you have a plotting function
#     # plot_data(df)
#     st.title("Feature Display")
#     st.subheader("Base Features")
#     st.write(load_features(BASE_FEATURES))
#     st.subheader("Base and Most Correlated Features")
#     st.write(load_features(BASE_AND_MOST_CORR_FEATURES))
#     st.subheader("Base and Least Correlated Features")
#     st.write(load_features(BASE_AND_LEAST_CORR_FEATURES))
# elif section == "Data Grid":
#     st.header("Data Grid")
#     st.write(df)
# elif section == "Forecast":
#     st.header("Forecast")
#     st.write("Forecasting models and results will be displayed here.")
# elif section == "More Analysis":
#     st.header("More Analysis")
#     st.write("Additional analysis and insights will be displayed here.")

# Credits

# Main app setup




st.sidebar.title("Credits")
st.sidebar.write("Developed by")
st.sidebar.write("CAI Qiaolong, Lu Yiwei,  O Kenglou, Ou Yifan ")

