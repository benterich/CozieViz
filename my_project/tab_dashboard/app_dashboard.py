from dash import dcc, html, Input, Output, callback
import pandas as pd

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
    
    # Convert the JSON back to a DataFrame
    try:
        df = pd.read_json(data_json, orient='split')
        columns = df.columns.tolist()
        return html.Ul([html.Li(col) for col in columns])
    except Exception as e:
        return html.Div(f"Error reading data: {str(e)}")
