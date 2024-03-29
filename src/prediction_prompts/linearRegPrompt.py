import pandas as pd
from dash import html
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml_models.modelLoading import load_model
from data_processing.dataProcessing import one_hot_encode_delivery_code
import dash_bootstrap_components as dbc


def linearRegressionPredictorLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with Linear Regression"),
        html.Div(
        [
            html.Br(),
            dbc.Input(id='number-of-students-linear', type='number', placeholder='Number of Students', style={'width': '15%'}),
            html.Br(),
            dbc.Input(id='exam-weight-linear', type='number', placeholder='Exam Weight', style={'width': '15%'}),
            html.Br(),
            dbc.Input(id='coursework-weight-linear', type='number', placeholder='Coursework Weight', style={'width': '15%'}),
            html.Br(),
            dbc.Input(id='delivery-code-linear', type='text', placeholder='Delivery Code', style={'width': '15%'}),
            html.Br(),
        ]),
        dbc.Button('Predict', color="secondary", id='linear-regression-prediction-button', n_clicks=0),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Div(id='linear-regression-prediction-output')
    ])

def linearRegressionPredictor(n_clicks, number_of_students, exam_weight, coursework_weight, delivery_code):
    if n_clicks > 0:
        # Prepare the input data in the format expected by the model
        input_data = pd.DataFrame([{
            'number_of_students': number_of_students,
            'exam_weight': exam_weight,
            'coursework_weight': coursework_weight,
            'delivery_code': delivery_code
        }])
        
        input_data = one_hot_encode_delivery_code(input_data)

        model = load_model('linear_model.pkl')

        # Ensure all columns from training data are present in input data (fill missing columns with 0s)
        missing_cols = set(model.feature_names_in_) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0
        # Reorder columns to match the training data
        input_data = input_data[model.feature_names_in_]

        # Make prediction
        prediction = model.predict(input_data)[0]
        return f"Predicted PGTA Hours: {prediction}"
    return ""