from dash import html, dcc
import dash_bootstrap_components as dbc
from my_project.tab_upload.app_upload import upload_function 
from my_project.tab_dashboard.app_dashboard import dashboard_function

def main():
    return html.Div([
        html.H2("CozieViz Main Page"),
        dbc.Button("Go to Dashboard", href="/dashboard", color="primary"),
        dbc.Button("Upload CSV", href="/upload", color="success")
    ])
