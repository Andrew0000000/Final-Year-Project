from dash import Dash, html, Output, Input, State, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from graphs.requestedVsRecruitedGraph import requestedVsRecruitedGraph, requestedVsRecruitedGraphLayout, moduleHistoryGraphLayout, moduleHistoryGraph
from graphs.variablesVsRecruitedGraph import studentsVsRecruitedGraphLayout, examWeightsVsRecruitedGraphLayout, deliveryCodeVsRecruitedGraphLayout
from graphs.dutiesVsPgtaHoursGraph import dutiesVsPGTAHoursGraphLayout, dutiesVsPGTAHoursGraph, dutiesVsPGTAHoursAverageGraphLayout
from prediction_prompts.linearRegPrompt import linearRegressionPredictor, linearRegressionPredictorLayout
from prediction_prompts.featureEngPrompt import featureEngineeringPredictor, featureEngineeringPredictorLayout
from prediction_prompts.vectoriserPrompt import vectoriserPredictor ,vectoriserPredictorLayout
from ml_models.modelTraining import retrainModels, retrainModelsLayout
from database.databaseLayout import displayTableLayout, displayTable, insertModuleLayout, insertModule, deleteModuleLayout, deleteModule
from sqlalchemy import create_engine

DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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

# # # # #   Home TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='Home', children=[

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Database Display', className='graph-title'),
                displayTableLayout(),
            ]),

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Insert Module', className='graph-title'),
                insertModuleLayout(),
            ]),

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Delete Module', className='graph-title'),
                deleteModuleLayout(),
            ]),

            html.Div(className='graph-spacing'),

        ], className='tab-style', selected_className='selected-tab-style'),

# # # # #   FIRST TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation


        dcc.Tab(label='Predictor', children=[

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Retrain Models', className='graph-title'),
                retrainModelsLayout(),
            ]),

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Regression Predictor', className='graph-title'),
                linearRegressionPredictorLayout(),
            ]),
            
            html.Div(className='graph-spacing'),
        
            html.Div(className='graph-container', children=[
                html.H3('NLP Predictor', className='graph-title'),
                featureEngineeringPredictorLayout(),
            ]),

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('NLP Predictor', className='graph-title'),
                vectoriserPredictorLayout(),
            ]),

            html.Div(className='graph-spacing'),

        ], className='tab-style', selected_className='selected-tab-style'),
    

# # # # #   SECOND TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='Module History', children=[

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Module History', className='graph-title'),
                moduleHistoryGraphLayout()
            ]),

            html.Div(className='graph-spacing'),

        ], className='tab-style', selected_className='selected-tab-style'),

# # # # #   THIRD TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation

        dcc.Tab(label='Variables Vs PGTAs Recruited', children=[

            html.Div(className='graph-spacing'),

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

        dcc.Tab(label='Duties Vs PGTA Hours Needed', children=[
            
            html.Div(className='graph-spacing'),
            
            html.Div(className='graph-container', children=[
                html.H3('Duties Vs PGTA Hours Needed', className='graph-title'),
                dutiesVsPGTAHoursGraphLayout()
            ]),
            
            html.Div(className='graph-spacing'),
            
            html.Div(className='graph-container', children=[
                html.H3('Average PGTA Hours for Each Duty', className='graph-title'),
                dutiesVsPGTAHoursAverageGraphLayout()
            ]),
            
            html.Div(className='graph-spacing'),

        ], className='tab-style', selected_className='selected-tab-style'),

# # # # #   FIFTH TAB   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Tab Separation


        dcc.Tab(label='PGTAs Requested vs Recruited', children=[

            html.Div(className='graph-spacing'),

            html.Div(className='graph-container', children=[
                html.H3('Requested vs Recruited', className='graph-title'),
                requestedVsRecruitedGraphLayout()
            ]),

            html.Div(className='graph-spacing'),

        ], className='tab-style', selected_className='selected-tab-style'),
    
    ])
])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for Table Display
@app.callback(
    Output("table-content", "children"),
    [Input("db-tabs", "active_tab")]
)

def update_displayTable(active_tab):
    return displayTable(active_tab)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for Insert Module
@app.callback(
    Output("insert-module-alert", "children"),
    [Input("insert-module-button", "n_clicks")],
    [State("module-code-insert", "value"),
    State("module-name-insert", "value"),
    State("number-of-students-insert", "value"),
    State("pgtas-recruited-insert", "value"),
    State("exam-weight-insert", "value"),
    State("coursework-weight-insert", "value"),
    State("delivery-code-insert", "value"),
    State("base-duties-checklist-insert", "value")]
)

def update_insertModule(n_clicks, module_code, module_name, number_of_students, pgtas_recruited, exam_weight, coursework_weight, delivery_code, duties):
    return insertModule(n_clicks, module_code, module_name, number_of_students, pgtas_recruited, exam_weight, coursework_weight, delivery_code, duties)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # Callback for Delete Module
@app.callback(
    Output("delete-module-alert", "children"),
    [Input("delete-module-button", "n_clicks")],
    [State("module-code-delete", "value")]
)

def update_deleteModule(n_clicks, module_code):
    return deleteModule(n_clicks, module_code)


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

# Callback for Duties Vs PGTA Hours Graph
@app.callback(
    Output(component_id='dutiesVsPGTAHoursGraph', component_property='figure'),
    Input(component_id='dutiesVsPGTAHoursGraphDropdown' , component_property='value')
)

def update_dutiesVsPGTAHoursGraph(selected_duty):
    return dutiesVsPGTAHoursGraph(selected_duty)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for Retain Models
@app.callback(
    Output('retrain-models-alert', 'children'),
    Input('retrain-models-button', 'n_clicks')
)

def update_retainModels(n_clicks):
    return retrainModels(n_clicks)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for Linear Regression Predictor Prompt
@app.callback(
    Output('regression-prediction-output', 'children'),
    [Input('regression-prediction-button', 'n_clicks')],
    [State('number-of-students', 'value'),
    State('exam-weight', 'value'),
    State('coursework-weight', 'value'),
    State('delivery-code', 'value')]
)

def update_linearRegressionPredictor(n_clicks, num_students, exam_weight, coursework_weight, delivery_code):
    return linearRegressionPredictor(n_clicks, num_students, exam_weight, coursework_weight, delivery_code)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for Feature Engineering Predictor Prompt
@app.callback(
    Output('feature-prediction-output', 'children'),
    [Input('feature-prediction-button', 'n_clicks')],
    [State('feature-base-duties-checklist', 'value')]
)

def update_featureEngineeringPredictor(n_clicks, selected_duties):
    return featureEngineeringPredictor(n_clicks, selected_duties)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Callback for Vectoriser Predictor Prompt
@app.callback(
    Output('vectoriser-prediction-output', 'children'),
    [Input('vectoriser-prediction-button', 'n_clicks')],
    [State('vectoriser-base-duties-checklist', 'value')]
)

def update_vectoriserPredictor(n_clicks, selected_duties):
    return vectoriserPredictor(n_clicks, selected_duties)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # Callback for Unified Predictor Prompt
# @app.callback(
#     Output('unified-prediction-output', 'children'),
#     [Input('unified-prediction-button', 'n_clicks')],
#     [State('unified-number-of-students', 'value'),
#     State('unified-exam-weight', 'value'),
#     State('unified-coursework-weight', 'value'),
#     State('unified-delivery-code', 'value'),
#     State('unified-base-duties-checklist', 'value')]
# )

# def update_unifiedPredictor(n_clicks, num_students, exam_weight, coursework_weight, delivery_code, selected_duties):
#     return unifiedPredictor(n_clicks, num_students, exam_weight, coursework_weight, delivery_code, selected_duties)

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

