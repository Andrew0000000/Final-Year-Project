from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from demoGraph import demoGraph, demoGraphLayout


app = Dash(__name__)

server = app.server

app.layout = html.Div([
    demoGraphLayout()
])

# Add controls to build the interaction
@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)

def update_graph(col_chosen):
    return demoGraph(col_chosen)


if __name__ == '__main__':
    app.run(debug=True)

