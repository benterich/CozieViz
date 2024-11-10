from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

def render_dashboard():
    return html.Div(className='container', children=[
        html.H2("Dashboard"),
        html.Div(id='dashboard-content')
    ])

@callback(
    Output('dashboard-content', 'children'),
    Input('uploaded-data-store', 'data')
)
def display_columns(data_json):
    if data_json is None:
        return html.Div("No data available. Please upload a CSV file first.")
    
    try:
        # Convert JSON data to DataFrame
        df = pd.read_json(data_json, orient='split')
        

        if 'index_time' not in df.columns or 'q_general_location_area' not in df.columns:
            return html.Div("Required columns not found in the data.")
        
        # Convert 'timestamp' column to datetime
        df['index_time'] = pd.to_datetime(df['index_time'], errors='coerce')
        
        # Drop rows with missing timestamps
        df = df.dropna(subset=['index_time'])
        
        # Filter out rows where 'q_general_location_area' is NaN
        df['q_general_location_area'] = df['q_general_location_area'].dropna()
        
        # Count the non-NaN responses over time
        df['date'] = df['index_time'].dt.date  # Extract date from index_time
        response_counts = df.groupby('date')['q_general_location_area'].count().reset_index()
        response_counts.columns = ['date', 'total_responses']
        
        # Create a line chart
        fig = px.line(
            response_counts, 
            x='date', 
            y='total_responses', 
            title='Accumulated Survey Responses Over Time',
            labels={'date': 'Date', 'total_responses': 'Total Responses'}
        )
        fig.update_layout(xaxis_title='Date', yaxis_title='Total Responses')

        # Display the chart
        return dcc.Graph(figure=fig)
    
    except Exception as e:
        return html.Div(f"Error reading data: {str(e)}")
