from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
import pandas as pd
import io
import base64
from my_project.routes import render_page_content, register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "CozieViz"

# Function to render the header
def render_header():
    return html.Div(
        className='header',
        children=[
            html.Div(
                className='logo',
                children=[
                    html.Img(src='/assets/img/cozie-logo-round.png', alt='Logo'),
                    html.H2("CozieViz", className='header-title')
                ]
            ),
            html.Div(
                className='documentation-links',
                children=[
                    html.A(
                        children=["Cozie", html.Img(src='/assets/icons/share.png', className='share-icon')],
                        href='https://cozie-apple.app/',
                        target='_blank',
                        className='doc-link'
                    ),
                    html.A(
                        children=["Cozie GitHub", html.Img(src='/assets/icons/share.png', className='share-icon')],
                        href='https://github.com/cozie-app/cozie-apple',
                        target='_blank',
                        className='doc-link'
                    ),
                    html.A(
                        children=["Cozie Research", html.Img(src='/assets/icons/share.png', className='share-icon')],
                        href='https://cozie.app/docs/cozie/intro-cozie/',
                        target='_blank',
                        className='doc-link'
                    )
                ]
            )
        ]
    )

# Function to render the tabs
def render_tabs(pathname):
    return html.Div(
        className='nav-tabs',
        children=[
            dcc.Link("Home", href="/", className='tab-link' + (' active' if pathname == '/' else '')),
            dcc.Link("Upload CSV", href="/upload", className='tab-link' + (' active' if pathname == '/upload' else '')),
            dcc.Link("Dashboard", href="/dashboard", className='tab-link' + (' active' if pathname == '/dashboard' else ''))
        ]
    )

# Function to render the footer
def render_footer():
    return html.Div(
        className='footer',
        children=["© 2024 CozieViz"]
    )

# Callback to update the tabs based on the current URL path
@app.callback(
    Output('nav-tabs', 'children'), 
    Input('url', 'pathname')
)
def update_tabs(pathname):
    return render_tabs(pathname)


# Callback to render the page content based on the current URL path
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    return render_page_content(pathname)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    render_header(),
    html.Div(id='nav-tabs'),
    dcc.Store(id='uploaded-data-store'),
    html.Div(id='page-content'),
    render_footer()
])

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
