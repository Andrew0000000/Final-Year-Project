import pandas as pd
from dash import html
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml_models.modelLoading import load_model
from data_processing.dataProcessing import one_hot_encode_delivery_code
import dash_bootstrap_components as dbc


def gamPredictorLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with Generalized Additive Model"),
        html.Div(
        [
            html.Br(),
            dbc.Input(id='number-of-students-gam', type='number', placeholder='Number of Students', style={'width': '15%'}),
            html.Br(),
            dbc.Input(id='exam-weight-gam', type='number', placeholder='Exam Weight', style={'width': '15%'}),
            html.Br(),
            dbc.Input(id='coursework-weight-gam', type='number', placeholder='Coursework Weight', style={'width': '15%'}),
            html.Br(),
            dbc.Input(id='delivery-code-gam', type='text', placeholder='Delivery Code', style={'width': '15%'}),
            html.Br(),
        ]),
        dbc.Button('Predict', color="secondary", id='gam-prediction-button', n_clicks=0),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Div(id='gam-prediction-output')
    ])

def gamPredictor(n_clicks, number_of_students, exam_weight, coursework_weight, delivery_code):
    if n_clicks > 0:
        input_data = pd.DataFrame([{
            'number_of_students': number_of_students,
            'exam_weight': exam_weight,
            'coursework_weight': coursework_weight,
            'delivery_code': delivery_code
        }])
        
        input_data = one_hot_encode_delivery_code(input_data)

        feature_names = ['number_of_students', 'exam_weight', 'coursework_weight', 'delivery_code_A4U', 'delivery_code_A5U', 'delivery_code_A6U', 'delivery_code_A7U', 'delivery_code_A7P']
        # Ensure all expected features are present in the input data, filling missing columns with 0s
        for feature in feature_names:
            if feature not in input_data.columns:
                input_data[feature] = 0
        
        # Reorder input_data columns to match the training feature order
        input_data = input_data[feature_names]

        gam = load_model('gam_model.pkl')
        prediction = gam.predict(input_data)
        return f"Predicted PGTA Hours with GAM: {prediction[0]}"
    return ""