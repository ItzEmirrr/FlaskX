import base64
import io
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from flask import Flask


server = Flask(__name__)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, server=server, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
        multiple=True  # Allow multiple files to be uploaded
    ),
    dcc.Store(id='stored-data'),  # Store for the uploaded data
    dcc.Dropdown(id='x-column-dropdown', placeholder='Select X-axis column'),
    dcc.Dropdown(id='y-column-dropdown', placeholder='Select Y-axis column'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    dcc.Graph(id='graph')
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return None
    return df


@app.callback(
    Output('stored-data', 'data'),
    Output('x-column-dropdown', 'options'),
    Output('y-column-dropdown', 'options'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)


def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        dfs = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names) if parse_contents(c, n) is not None]
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            options = [{'label': col, 'value': col} for col in df.columns]
            return df.to_json(date_format='iso', orient='split'), options, options
    return None, [], []


@app.callback(
    Output('graph', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('x-column-dropdown', 'value'),
    State('y-column-dropdown', 'value'),
    State('stored-data', 'data')
)


def update_graph(n_clicks, x_column, y_column, json_data):
    if n_clicks > 0 and json_data is not None and x_column and y_column:
        df = pd.read_json(json_data, orient='split')
        fig = px.scatter(df, x=x_column, y=y_column)
        return fig
    return {}



@server.route('/')
def render_dash():
    return app.index()



if __name__ == '__main__':
    server.run(debug=True)

