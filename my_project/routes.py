from dash import html, dcc
from my_project.tab_upload.app_upload import render_upload, register_upload_callbacks
from my_project.tab_dashboard.app_dashboard import render_dashboard, display_columns

def register_callbacks(app):
    register_upload_callbacks(app)
    display_columns(app) 

def render_page_content(pathname):
    if pathname == '/upload':
        return render_upload()
    elif pathname == '/dashboard':
        return render_dashboard()
    else:
        return render_home()

def render_home():
    return html.Div(className='container', children=[
        html.H2("Welcome to CozieViz Dashboard"),
        html.P("This tool helps you upload CSV files and visualize the data.")
    ])
