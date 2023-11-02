from dash import Dash, html, Output, Input
from demoGraph import demoGraph, demoGraphLayout
from capAndActualGraph import capAndActualGraph, capAndActualGraphLayout

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    demoGraphLayout(),
    capAndActualGraphLayout()
])

# Callback for demoGraph
@app.callback(
    Output(component_id='demoGraph', component_property='figure'),
    Input(component_id='demoGraphRadioItem', component_property='value')
)


def update_demo_graph(col_chosen):
    return demoGraph(col_chosen)

def update_cap_and_actual_graph():
    return capAndActualGraph()

if __name__ == '__main__':
    app.run(debug=True)
