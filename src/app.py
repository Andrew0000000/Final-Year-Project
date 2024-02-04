from dash import Dash, html, Output, Input, State, dcc
import dash_daq as daq
from graphs.requestedVsRecruitedGraph import requestedVsRecruitedGraph, requestedVsRecruitedGraphLayout, moduleHistoryGraphLayout, moduleHistoryGraph
from graphs.variablesVsRecruitedGraph import studentsVsRecruitedGraphLayout, examWeightsVsRecruitedGraphLayout, deliveryCodeVsRecruitedGraphLayout
from prediction_prompt.predictionPrompt import predict, predictorGraphLayout
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

# # # # #   FIRST TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='PGTAs Requested vs Recruited', children=[
            html.Div(className='graph-container', children=[
                html.H3('Requested vs Recruited', className='graph-title'),
                requestedVsRecruitedGraphLayout()
            ])
        ], className='tab-style', selected_className='selected-tab-style'),

# # # # #   SECOND TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='Module History', children=[
            html.Div(className='graph-container', children=[
                html.H3('Module History', className='graph-title'),
                moduleHistoryGraphLayout()
            ]),
            html.Div(className='graph-spacing'),
        ], className='tab-style', selected_className='selected-tab-style'),

# # # # #   THIRD TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='Variables Vs PGTAs Recruited', children=[

            html.Div(className='graph-container', children=[
                html.H3('Students Vs PGTAs Recruited for 2022-2023', className='graph-title'),
                studentsVsRecruitedGraphLayout()
            ]),
            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Exam:Coursework Weight Ratio Vs PGTAs Recruited for 2022-2023', className='graph-title'),
                examWeightsVsRecruitedGraphLayout()
            ]),
            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Delivery Code Vs PGTAs Recruited for 2022-2023', className='graph-title'),
                deliveryCodeVsRecruitedGraphLayout()
            ]),
            html.Div(className='graph-spacing'),
        ], className='tab-style', selected_className='selected-tab-style'),

# # # # #   FOURTH TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='Predictor', children=[
            html.Div(className='graph-container', children=[
                html.H3('Predictor', className='graph-title'),
                predictorGraphLayout(),
            ]),
            html.Div(className='graph-spacing'),
        ], className='tab-style', selected_className='selected-tab-style'),

    ])
])



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

# Callback for PredictionCallback
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('number-of-students', 'value'),
    State('exam-weight', 'value'),
    State('coursework-weight', 'value'),
    State('delivery-code', 'value')]
)

def update_prediction(n_clicks, num_students, exam_weight, coursework_weight, delivery_code):
    return predict(n_clicks, num_students, exam_weight, coursework_weight, delivery_code)

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
