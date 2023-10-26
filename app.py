from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('MockData.csv')


app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)

def update_graph(col_chosen):
    fig = px.histogram(df, x='country', y=col_chosen)
    return fig

if __name__ == '__main__':
    app.run(debug=True)

