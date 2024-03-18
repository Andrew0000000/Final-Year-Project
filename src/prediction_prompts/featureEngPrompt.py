import pandas as pd
import os
import sys
from dash import html
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml_models.modelLoading import load_model
from data_processing.dataframeCleaning import duties
import dash_bootstrap_components as dbc

model = load_model('feature_engineering_model.pkl')

def featureEngineeringPredictorLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with Feature Engineering"),
        html.Div([
            dbc.Checklist(
            id="feature-base-duties-checklist",
            value=[],
            options=[{'label': duty, 'value': duty} for duty in duties],
            ),
        ]),
        html.Br(),
        dbc.Button('Predict', color="secondary", id='feature-prediction-button', n_clicks=0),
        html.Hr(),
        html.Br(),
        html.Div(id='feature-prediction-output')
    ])

def featureEngineeringPredictor(n_clicks, selected_duties):
    if n_clicks > 0:
        # prepare the input data in the format expected by the model
        data = {duty: 0 for duty in duties}
        for duty in selected_duties:
            data[duty] = 1
        
        input_data = pd.DataFrame([data])
        
        # fill missing columns with 0s
        missing_cols = set(model.feature_names_in_) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0

        # reorder columns to match the training data
        input_data = input_data[model.feature_names_in_]
        
        # make prediction
        prediction = model.predict(input_data)[0]
        return f"Predicted PGTA Hours: {prediction}"
    return ""