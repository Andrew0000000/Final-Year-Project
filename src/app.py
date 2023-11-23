from dash import Dash, html, Output, Input, State, dcc
import dash_daq as daq
from demoGraph import demoGraph, demoGraphLayout
from requestedVsRecruitedGraph import requestedVsRecruitedGraph, requestedVsRecruitedGraphLayout, moduleHistoryGraphLayout, moduleHistoryGraph, stats_layout
from variablesVsRecruitedGraph import studentsVsRecruitedGraph, studentsVsRecruitedGraphLayout
app = Dash(__name__)
server = app.server

app.layout = html.Div(id='dark-theme-components', style={
        'border': 'solid 1px #A2B1C6',
        'border-radius': '10px',
        'padding': '40px',
        'marginTop': '10px'
    }, children=[

    daq.ToggleSwitch(
        id='toggle-theme',
        label=['Light', 'Dark'],
        value=True
    ),

    html.Div(className='graph-spacing'),

    dcc.Tabs(className='tabs-styles', children=[
        dcc.Tab(label='Demo Graph', children=[
            html.Div(className='graph-container', children=[
                html.H3('Demo', className='graph-title'),
                demoGraphLayout()
            ])
        ], className='tab-style', selected_className='selected-tab-style'),

        dcc.Tab(label='PGTAs Requested vs Recruited', children=[
            html.Div(className='graph-container', children=[
                html.H3('Requested vs Recruited', className='graph-title'),
                requestedVsRecruitedGraphLayout()
            ])
        ], className='tab-style', selected_className='selected-tab-style'),

        dcc.Tab(label='Module History', children=[
            html.Div(className='graph-container', children=[
                html.H3('Module History', className='graph-title'),
                moduleHistoryGraphLayout()
            ]),
            html.Div(className='graph-spacing'),
            stats_layout
        ], className='tab-style', selected_className='selected-tab-style'),

        dcc.Tab(label='Variables Vs PGTAs Recruited', children=[
            html.Div(className='graph-container', children=[
                html.H3('Students Vs PGTAs Recruited for 2022-2023', className='graph-title'),
                studentsVsRecruitedGraphLayout()
            ]),
            html.Div(className='graph-spacing'),
        ], className='tab-style', selected_className='selected-tab-style'),
    ])
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for toggling between light and dark theme
@app.callback(
    Output('dark-theme-components', 'style'),
    Input('toggle-theme', 'value'),
    State('dark-theme-components', 'style')
)

def switch_bg(dark, currentStyle):
    if(dark):
        currentStyle.update(backgroundColor='#303030')
    else:
        currentStyle.update(backgroundColor='white')
    return currentStyle

if __name__ == '__main__':
    app.run(debug=True)
