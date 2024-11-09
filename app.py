import os
import pandas as pd
import io
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from my_project.routes import main
import base64

# Initialize the Dash app with suppress_callback_exceptions
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "CozieViz"

UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store column names
uploaded_columns = []

# Define the layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define the navigation menu
nav = dbc.Nav(
    [
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Upload CSV", href="/upload", active="exact"),
        dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
    ],
    pills=True,
)

# Define content for different pages
def render_home():
    return html.Div([
        html.H2("Welcome to CozieViz Dashboard"),
        html.P("This tool helps you upload CSV files and visualize the data."),
        nav
    ])

def render_upload():
    return html.Div([
        html.H2("Upload a CSV File"),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload CSV', className='btn btn-primary'),
            multiple=False
        ),
        html.Div(id='upload-message', style={'margin-top': '20px'}),
        nav
    ])

def render_dashboard():
    if not uploaded_columns:
        return html.Div([
            html.H2("No data available"),
            html.P("Please upload a CSV file first."),
            nav
        ])
    return html.Div([
        html.H2("Dashboard"),
        html.H4("Column Names:"),
        html.Ul([html.Li(col) for col in uploaded_columns]),
        nav
    ])

# Page routing callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/upload':
        return render_upload()
    elif pathname == '/dashboard':
        return render_dashboard()
    else:
        return render_home()

# File upload handling callback
@app.callback(
    Output('upload-message', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def handle_upload(contents, filename):
    global uploaded_columns
    if contents is None:
        return ""
    
    try:
        # Decode the base64 content
        content_type, content_string = contents.split(',')
        decoded_string = base64.b64decode(content_string).decode('utf-8')

        # Use StringIO to read the CSV content
        decoded = pd.read_csv(io.StringIO(decoded_string))

        # Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        decoded.to_csv(filepath, index=False)

        # Extract column names
        uploaded_columns = decoded.columns.tolist()
        return f'File "{filename}" uploaded successfully!'
    
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
