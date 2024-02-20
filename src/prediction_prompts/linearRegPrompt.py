import pandas as pd
from dash import html, dcc
from models.modelLoading import load_model
import os 
import sys

# select whether to use linear regression or ridge regression by switching model_type between 'linear' or 'ridge'
model_type = 'ridge'
project_base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
model = load_model(f'{model_type}_model.pkl')

def linearRegPredictorGraphLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with Ridge Regression"),
    
        dcc.Input(id='number-of-students', type='number', placeholder='Number of Students'),
        dcc.Input(id='exam-weight', type='number', placeholder='Exam Weight'),
        dcc.Input(id='coursework-weight', type='number', placeholder='Coursework Weight'),
        dcc.Input(id='delivery-code', type='text', placeholder='Delivery Code'),
        
        html.Button('Predict', id='predict-button', n_clicks=0),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Div(id='prediction-output')
    ])

def linear_regression_predict(n_clicks, num_students, exam_weight, coursework_weight, delivery_code):
    if n_clicks > 0:
        # Prepare the input data in the format expected by the model
        input_data = pd.DataFrame([{
            'Number of Students': num_students,
            'Exam Weight': exam_weight,
            'Coursework Weight': coursework_weight,
            'Delivery Code': delivery_code
        }])

        # Convert 'Delivery Code' to dummy variables
        input_data = pd.get_dummies(input_data)

        # Ensure all columns from training data are present in input data (fill missing columns with 0s)
        missing_cols = set(model.feature_names_in_) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0
        # Reorder columns to match the training data
        input_data = input_data[model.feature_names_in_]

        # Make prediction
        prediction = model.predict(input_data)[0]
        return f"Predicted PGTAs Recruited: {prediction}"
    return ""