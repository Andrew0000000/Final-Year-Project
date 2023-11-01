import pandas as pd
import plotly.express as px
from dash import html, dash_table, dcc


df = pd.read_csv('../data/MockData.csv')

def demoGraph(col_chosen):
    fig = px.histogram(df, x='country', y=col_chosen)
    return fig

def demoGraphLayout():
    return html.Div([
        html.H1(children='My First App with Data, Graph, and Controls'),
        html.Hr(),
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
        dash_table.DataTable(data=pd.read_csv('../data/MockData.csv').to_dict('records'), page_size=10),
        dcc.Graph(figure={}, id='controls-and-graph')
    ])

