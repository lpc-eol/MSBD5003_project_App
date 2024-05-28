import streamlit as st
import pymongo
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
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
    df['Combo'] = df['Dataset'] + " + " + df['Features']
    return df

def plot_accuracy_histogram(df):
    models = df['Model'].unique()
    fig = make_subplots(rows=1, cols=len(models), subplot_titles=models)
    
    # Determine a uniform Y-axis range
    max_accuracy = df['Accuracy'].max()

    for i, model in enumerate(models, start=1):
        model_data = df[df['Model'] == model]
        for combo in model_data['Combo'].unique():
            subset = model_data[model_data['Combo'] == combo]
            fig.add_trace(
                go.Bar(x=[model], y=subset['Accuracy'], name=combo),
                row=1, col=i
            )
        # Apply uniform Y-axis range
        fig.update_yaxes(title="Accuracy (%)" if i == 1 else "", row=1, col=i, range=[0, max_accuracy + 5])

    fig.update_layout(barmode='group', title_text='Accuracy per Model Configuration',
                      showlegend=True, title_font=dict(size=24, color='white'), legend_title_text='Dataset + Features')
    
    return fig

def plot_loss_histogram(df):
    loss_types = ['RMSE', 'MSE', 'MAE', 'MAPE']
    models = df['Model'].unique()
    # Adjusting column widths for spacing between groups
    # Each group is given a width of 0.2 and spacing of 0.05 between them.
    fig = make_subplots(rows=1, cols=len(loss_types), subplot_titles=loss_types,
                        column_widths=[0.2, 0.2, 0.2, 0.2], horizontal_spacing=0.08)
    
    for i, loss_type in enumerate(loss_types, start=1):
        if loss_type in df.columns:
            for model in models:
                model_data = df[df['Model'] == model]
                if loss_type in model_data.columns:
                    trace_name = f"{model}_{loss_type}"  # E.g., LR_RMSE
                    fig.add_trace(
                        go.Bar(x=[model], y=model_data[loss_type], name=trace_name),
                        row=1, col=i
                    )
            
            # Use auto-ranging for the Y-axis to dynamically adjust based on data
            fig.update_yaxes(
                title=f"{loss_type} Value" if i == 1 else "",
                row=1, col=i,
                autorange=True,  # Automatically determines the best range
                type='linear'  # Ensuring linear scale
            )

    fig.update_layout(
        barmode='group',
        title_text='Loss Comparison across Models',
        showlegend=True,
        title_font=dict(size=24, color='white'),
        legend_title_text='Model + Loss',
        plot_bgcolor='rgba(0,0,0,0)',  # Transparency for plot background
        margin=dict(l=20, r=20, t=100, b=20),  # Adjust margins to ensure everything fits
        separators='.,'  # Use period as decimal and comma as thousands separator
    )
    return fig


def main():
    st.title("Evaluation result on Testing Data")

    db_name = "bitcoinprice"
    collection_name = "final"

    data = fetch_data(db_name, collection_name)

    if data:
        df = prepare_data_for_accuracy(data)
        accuracy_fig = plot_accuracy_histogram(df)
        st.plotly_chart(accuracy_fig, use_container_width=True)
        
        df_loss = pd.DataFrame(data)
        df_loss = abbreviate_model_names(df_loss)
        loss_fig = plot_loss_histogram(df_loss)
        st.plotly_chart(loss_fig, use_container_width=True)
    else:
        st.write("No data found or unable to connect to MongoDB.")

if __name__ == "__main__":
    main()
