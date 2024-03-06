import pandas as pd
import os
import sys
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml_models.modelLoading import load_model
from data_processing.dataframeCleaning import duties
import dash_bootstrap_components as dbc

# load the feature engineering model
model_type = 'feature_engineering'
model = load_model(f'{model_type}_model.pkl')

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
        input_data = {duty: 0 for duty in duties}
        for duty in selected_duties:
            input_data[duty] = 1
        
        input_df = pd.DataFrame([input_data])
        
        # fill missing columns with 0s
        missing_cols = set(model.feature_names_in_) - set(input_df.columns)
        for col in missing_cols:
            input_df[col] = 0

        # reorder columns to match the training data
        input_df = input_df[model.feature_names_in_]
        
        # make prediction
        prediction = model.predict(input_df)[0]
        return f"Predicted PGTA Hours: {prediction}"
    return ""