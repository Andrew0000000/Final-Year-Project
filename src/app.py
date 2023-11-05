from dash import Dash, html, Output, Input
from demoGraph import demoGraph, demoGraphLayout
from requestedVsRecruitedGraph import requestedVsRecruitedGraph, requestedVsRecruitedGraphLayout

app = Dash(__name__)
server = app.server


app.layout = html.Div([
    demoGraphLayout(),
    html.Hr(),
    requestedVsRecruitedGraphLayout()
])

# Callback for demoGraph
@app.callback(
    Output(component_id='demoGraph', component_property='figure'),
    Input(component_id='demoGraphRadioItem', component_property='value')
)

# Callback for requestedVsRecruitedGraph

def update_demoGraph(col_chosen):
    return demoGraph(col_chosen)

@app.callback(
    Output(component_id='requestedVsRecruitedGraph', component_property='figure'),
    Input(component_id='requestedVsRecruitedGraphDropdown' , component_property='value')
)

def update_requestedVsRecruitedGraph(selected_year):
    return requestedVsRecruitedGraph(selected_year)

if __name__ == '__main__':
    app.run(debug=True)
