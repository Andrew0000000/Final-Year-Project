import pandas as pd
import os
import sys
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml_models.modelLoading import load_model
from data_processing.dataframeCleaning import duties

# load the feature engineering model
model_type1 = 'feature_engineering'
model_type2 = 'ridge'
model1 = load_model(f'{model_type1}_model.pkl')
model2 = load_model(f'{model_type2}_model.pkl')


def unifiedPredictorLayout():
    return html.Div([
        html.H1("PGTA Recruitment Unified Predictor"),
        # Inputs for structured parameters
        dcc.Input(id='number-of-students', type='number', placeholder='Number of Students'),
        dcc.Input(id='exam-weight', type='number', placeholder='Exam Weight'),
        dcc.Input(id='coursework-weight', type='number', placeholder='Coursework Weight'),
        dcc.Input(id='delivery-code', type='text', placeholder='Delivery Code'),
        # Checklist for duties
        html.Div([
            dcc.Checklist(
                id='duties-checklist',
                options=[{'label': duty, 'value': duty} for duty in duties],
                value=[],
                labelStyle={'display': 'block'}
            ),
        ]),
        html.Button('Predict', id='unified-prediction-button', n_clicks=0),
        html.Div(id='unified-prediction-output')
    ])


def unifiedPredictor(n_clicks, num_students, exam_weight, coursework_weight, delivery_code, selected_duties):
    if n_clicks > 0:
        # Prepare the input data in the format expected by the model
        input_data = pd.DataFrame([{
            'Number of Students': num_students,
            'Exam Weight': exam_weight,
            'Coursework Weight': coursework_weight,
            'Delivery Code': delivery_code
        }])
        for duty in selected_duties:
            input_data[duty] = 1
        
        # Convert 'Delivery Code' to dummy variables
        input_data = pd.get_dummies(input_data)

        # Ensure all columns from training data are present in input data (fill missing columns with 0s)
        missing_cols = set(model2.feature_names_in_) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0
        # Reorder columns to match the training data
        input_data = input_data[model2.feature_names_in_]

        # Make prediction
        prediction = model2.predict(input_data)[0]
        return f"Predicted PGTAs Recruited: {prediction}"
    return ""