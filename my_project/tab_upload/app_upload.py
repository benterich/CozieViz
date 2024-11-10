from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import io
import base64

uploaded_df = None

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

# Callback to handle file upload and store it in the dcc.Store component
def register_upload_callbacks(app):
    @app.callback(
        Output('upload-message', 'children'),
        Output('uploaded-data-store', 'data'),
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def handle_upload(contents, filename):
        global uploaded_df
        if contents is None:
            return "", None
        
        try:
            content_type, content_string = contents.split(',')
            decoded_string = base64.b64decode(content_string).decode('utf-8')
            uploaded_df = pd.read_csv(io.StringIO(decoded_string))
            
            # Convert DataFrame to JSON to store in dcc.Store
            data_json = uploaded_df.to_json(orient='split')
            return f'File "{filename}" uploaded successfully!', data_json
        except Exception as e:
            return f"Error processing file: {str(e)}", None
