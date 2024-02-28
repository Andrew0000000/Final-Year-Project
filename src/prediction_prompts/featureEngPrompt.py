import pandas as pd
import os
import sys
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ml_models.modelLoading import load_model
from data_processing.dataProcessing import get_set_of_duties

filePath_jobDescriptionData = '../data/jobDescriptionData.csv'
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
base_duties = get_set_of_duties(df_jobDescriptionData['Duties'])

# load the feature engineering model
model_type = 'feature_engineering'
model = load_model(f'{model_type}_model.pkl')

def featureEngineeringPredictorLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with Feature Engineering"),
        
        # create radio items for each base duty
        html.Div([
            dcc.Checklist(
                id='feature-base-duties-checklist',
                options=[{'label': duty, 'value': duty} for duty in base_duties],
                value=[],
                labelStyle={'display': 'block'}
            ),
        ]),
        html.Br(),
        html.Button('Predict', id='feature-prediction-button', n_clicks=0),
        html.Hr(),
        html.Br(),
        html.Div(id='feature-prediction-output')
    ])

def featureEngineeringPredictor(n_clicks, selected_duties):
    if n_clicks > 0:
        # prepare the input data in the format expected by the model
        input_data = {duty: 0 for duty in base_duties}
        for duty in selected_duties:
            input_data[duty] = 1
        
        input_df = pd.DataFrame([input_data])
        
        # fill missing columns with 0s
        missing_cols = set(model.feature_names_in_) - set(input_df.columns)
        for col in missing_cols:
            input_df[col] = 0

        # reorder columns to match the training data
        input_df = input_df[model.feature_names_in_]
        print(input_df)
        # make prediction
        prediction = model.predict(input_df)[0]
        return f"Predicted PGTAs Recruited: {prediction}"
    return ""