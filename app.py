from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
import pandas as pd
import io
import base64

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "CozieViz"


uploaded_df = None


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
                        children=[
                            "Cozie",
                            html.Img(src='/assets/icons/share.png', alt='Share Icon', className='share-icon')
                        ],
                        href='https://cozie-apple.app/',
                        target='_blank',
                        className='doc-link'
                    ),
                    html.A(
                        children=[
                            "Cozie GitHub",
                            html.Img(src='/assets/icons/share.png', alt='Share Icon', className='share-icon')
                        ],
                        href='https://github.com/cozie-app/cozie-apple',
                        target='_blank',
                        className='doc-link'
                    ),
                    html.A(
                        children=[
                            "Cozie Research",
                            html.Img(src='/assets/icons/share.png', alt='Share Icon', className='share-icon')
                        ],
                        href='https://cozie.app/docs/cozie/intro-cozie/',
                        target='_blank',
                        className='doc-link'
                    )
                ]
            )
        ]
    )

def render_footer():
    return html.Div(
        className='footer',
        children=["© 2024 CozieViz"]
    )

def render_tabs(pathname):
    return html.Div(
        className='nav-tabs',
        children=[
            dcc.Link("Home", href="/", className='tab-link' + (' active' if pathname == '/' else '')),
            dcc.Link("Upload CSV", href="/upload", className='tab-link' + (' active' if pathname == '/upload' else '')),
            dcc.Link("Dashboard", href="/dashboard", className='tab-link' + (' active' if pathname == '/dashboard' else ''))
        ]
    )

def render_home():
    return html.Div(className='container', children=[
        html.H2("Welcome to CozieViz Dashboard"),
        html.P("This tool helps you upload CSV files and visualize the data.")
    ])

def render_upload():
    return html.Div(className='container', children=[
        html.H2("Upload a CSV File"),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload CSV', className='btn btn-primary'),
            multiple=False
        ),
        html.Div(id='upload-message', style={'margin-top': '20px'})
    ])

def render_dashboard():
    return html.Div(className='container', children=[
        html.H2("Dashboard"),
        html.P("Data visualization and analysis.")
    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    render_header(),
    html.Div(id='nav-tabs'),
    html.Div(id='page-content'),
    render_footer()
])

@app.callback(
    Output('nav-tabs', 'children'),
    Input('url', 'pathname')
)
def update_tabs(pathname):
    return render_tabs(pathname)

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

@app.callback(
    Output('upload-message', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def handle_upload(contents, filename):
    global uploaded_df
    if contents is None:
        return ""
    
    try:
        # Decode the uploaded file content
        content_type, content_string = contents.split(',')
        decoded_string = base64.b64decode(content_string).decode('utf-8')
        # Read the CSV into a DataFrame
        uploaded_df = pd.read_csv(io.StringIO(decoded_string))
        
        # Return success message
        return f'File "{filename}" read successfully!'

    except Exception as e:
        return f"Error processing file: {str(e)}"

def render_dashboard():
    global uploaded_df
    if uploaded_df is None or uploaded_df.empty:
        return html.Div(className='container', children=[
            html.H2("No data available"),
            html.P("Please upload a CSV file first.")
        ])
    
    # Display the column names
    column_list = uploaded_df.columns.tolist()
    return html.Div(className='container', children=[
        html.H2("Dashboard"),
        html.H4("Uploaded CSV Column Names:"),
        html.Ul([html.Li(col) for col in column_list])
    ])




if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
