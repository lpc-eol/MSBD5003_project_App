import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import plotly.graph_objects as go

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

def fetch_data(db_name, collection_name):
    if client is not None:
        db = client[db_name]
        collection = db[collection_name]
        data = list(collection.find({}))
        return data
    else:
        st.error("No MongoDB client available.")
        return []


def abbreviate_model_names(df):
    model_abbreviations = {
        "GeneralizedLinearRegression": "GLR",
        "GradientBoostingTreeRegressor": "GBTR",
        "LinearRegression": "LR",
        "RandomForestRegressor": "RFR",
    }
    df['Model'] = df['Model'].map(model_abbreviations).fillna(df['Model'])
    return df


def prepare_data_for_accuracy(data):
    df = pd.DataFrame(data)
    df = abbreviate_model_names(df)
    return df

def remove_outliers(df, column, threshold=3):
    """
    Remove outliers from a DataFrame column using the standard deviation method.

    Args:
        df: DataFrame containing the data
        column: Name of the column to remove outliers from
        threshold: Number of standard deviations from the mean to consider as an outlier

    Returns:
        DataFrame with outliers removed
    """
    mean = df[column].mean()
    std_dev = df[column].std()
    lower_bound = mean - threshold * std_dev
    upper_bound = mean + threshold * std_dev

    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


def prepare_data(data):
    df = pd.DataFrame(data)
    df = abbreviate_model_names(df)
    # Remove outliers for 'RMSE' and 'R2' before plotting
    if 'RMSE' in df.columns:
        df = remove_outliers(df, 'RMSE')
    if 'R2' in df.columns:
        df = remove_outliers(df, 'R2')
    return df

def plot_rmse_histogram(df):
    rmse_title = 'RMSE per Model type'
    fig_rmse = px.bar(df, x="Model", y="RMSE", color="Type", facet_col="Splitting", title=rmse_title)
    fig_rmse.update_layout(barmode='group')
    fig_rmse.update_layout(title_font=dict(size=24, color='white'))
    fig_rmse.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig_rmse


def plot_r2_histogram(df):
    rmse_title = 'R2 per Model type'
    fig_rmse = px.bar(df, x="Model", y="R2", color="Type", facet_col="Splitting", title=rmse_title)
    fig_rmse.update_layout(barmode='group')
    fig_rmse.update_layout(title_font=dict(size=24, color='white'))
    fig_rmse.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig_rmse


# def plot_rmse_histogram(df):
#     rmse_title = 'RMSE per Model Type'
#     fig = make_subplots(rows=1, cols=len(df['Splitting'].unique()), subplot_titles=df['Splitting'].unique())
    
#     for i, split in enumerate(df['Splitting'].unique(), start=1):
#         split_data = df[df['Splitting'] == split]
#         max_rmse = split_data['RMSE'].max()
#         fig.add_trace(
#             go.Bar(x=split_data['Model'], y=split_data['RMSE'], name='RMSE', marker_color=px.colors.qualitative.Plotly),
#             row=1, col=i
#         )
#         # Dynamically adjust Y-axis based on the data
#         fig.update_yaxes(title="RMSE", row=1, col=i, range=[0, max_rmse + max_rmse * 0.1])

#     fig.update_layout(barmode='group', title_text=rmse_title, showlegend=True, title_font=dict(size=24, color='white'))
#     return fig

# def plot_r2_histogram(df):
#     r2_title = 'R2 per Model Type'
#     fig = make_subplots(rows=1, cols=len(df['Splitting'].unique()), subplot_titles=df['Splitting'].unique())
    
#     for i, split in enumerate(df['Splitting'].unique(), start=1):
#         split_data = df[df['Splitting'] == split]
#         max_r2 = split_data['R2'].max()
#         fig.add_trace(
#             go.Bar(x=split_data['Model'], y=split_data['R2'], name='R2', marker_color=px.colors.qualitative.Plotly),
#             row=1, col=i
#         )
#         # Dynamically adjust Y-axis based on the data
#         fig.update_yaxes(title="R2", row=1, col=i, range=[0, max_r2 + max_r2 * 0.1])

#     fig.update_layout(barmode='group', title_text=r2_title, showlegend=True, title_font=dict(size=24, color='white'))
#     return fig

def plot_accuracy_histogram(df):
    accuracy_title = 'Accuracy Comparison between Default and Tuned Models'
    splitting_methods = df['Splitting'].unique()
    
    # Initialize the figure with subplots
    fig = make_subplots(rows=1, cols=len(splitting_methods), subplot_titles=splitting_methods)
    
    # Variable to hold the maximum accuracy value across all subplots
    new_max_value = 0
    
    # Add traces for each split and update the maximum value dynamically
    for i, split in enumerate(splitting_methods, start=1):
        split_data = df[df['Splitting'] == split]
        fig.add_trace(
            go.Bar(x=split_data['Model'], y=split_data['Accuracy (default)'], name='Default', marker_color='blue'),
            row=1, col=i
        )
        fig.add_trace(
            go.Bar(x=split_data['Model'], y=split_data['Accuracy (tuned)'], name='Tuned', marker_color='red'),
            row=1, col=i
        )
        
        # Update the maximum accuracy value if the current split has higher values
        current_max = split_data[['Accuracy (default)', 'Accuracy (tuned)']].max().max()
        if new_max_value < current_max:
            new_max_value = current_max

    # Set the uniform Y-axis range after finding the maximum value across all splits
    for i in range(1, len(splitting_methods) + 1):
        fig.update_yaxes(title="Accuracy (%)" if i == 1 else "", row=1, col=i, range=[0, new_max_value + 5], dtick=10)

    # Update layout settings for the entire figure
    fig.update_layout(barmode='group', title_text=accuracy_title, showlegend=True, title_font=dict(size=24, color='white'))
    return fig



def main():
    st.title("Analysis & Comparison Between different Model Type on Training Set")

    db_name = "bitcoinprice"
    collection_name = "all"
    collection2_name = "accuracy"

    data_for_all = fetch_data(db_name, collection_name)
    data_for_accuracy = fetch_data(db_name, collection2_name)

    if data_for_all:
        df = prepare_data(data_for_all)
        fig_rmse = plot_rmse_histogram(df)
        st.plotly_chart(fig_rmse, use_container_width=True)
        fig_r2 = plot_r2_histogram(df)
        st.plotly_chart(fig_r2, use_container_width=True)
    if data_for_accuracy:
        df_accuracy = prepare_data_for_accuracy(data_for_accuracy)
        fig = plot_accuracy_histogram(df_accuracy)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data found or unable to connect to MongoDB.")

if __name__ == "__main__":
    main()
