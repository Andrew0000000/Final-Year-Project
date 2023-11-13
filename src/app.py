from dash import Dash, html, Output, Input
from demoGraph import demoGraph, demoGraphLayout
from requestedVsRecruitedGraph import requestedVsRecruitedGraph, requestedVsRecruitedGraphLayout, moduleHistoryGraphLayout, moduleHistoryGraph

app = Dash(__name__)
server = app.server


app.layout = html.Div([
    demoGraphLayout(),
    html.Hr(),
    requestedVsRecruitedGraphLayout(),
    html.Hr(),
    moduleHistoryGraphLayout()
])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for demoGraph
@app.callback(
    Output(component_id='demoGraph', component_property='figure'),
    Input(component_id='demoGraphRadioItem', component_property='value')
)

def update_demoGraph(col_chosen):
    return demoGraph(col_chosen)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for requestedVsRecruitedGraph
@app.callback(
    Output(component_id='requestedVsRecruitedGraph', component_property='figure'),
    Input(component_id='requestedVsRecruitedGraphDropdown' , component_property='value')
)

def update_requestedVsRecruitedGraph(selected_year):
    return requestedVsRecruitedGraph(selected_year)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for moduleHistoryGraph
@app.callback(
    Output(component_id='moduleHistoryGraph', component_property='figure'),
    Input(component_id='moduleHistoryGraphDropdown' , component_property='value')
)

def update_moduleHistoryGraph(selected_module):
    return moduleHistoryGraph(selected_module)

if __name__ == '__main__':
    app.run(debug=True)
