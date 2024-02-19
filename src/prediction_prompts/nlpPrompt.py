import pandas as pd
from dash import html, dcc
from models.modelLoading import load_model
import os 
from data_processing.dataProcessing import get_set_of_duties


project_base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
filePath_jobDescriptionData = os.path.join(project_base_path, 'data/jobDescriptionData.csv')
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
base_duties = get_set_of_duties(df_jobDescriptionData['Duties'])

# Load the feature engineering model
model_type = 'feature_engineering'
model = load_model(f'{model_type}_model.pkl')


def featureEngPredictorGraphLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with Feature Engineering"),
        
        # Create radio items for each base duty
        html.Div([
            dcc.Checklist(
                id='base-duties-checklist',
                options=[{'label': duty, 'value': duty} for duty in base_duties],
                value=[],
                labelStyle={'display': 'block'}
            ),
        ]),
        html.Br(),
        html.Button('Predict', id='predict-feature-button', n_clicks=0),
        html.Hr(),
        html.Br(),
        html.Div(id='prediction-feature-output')
    ])

def feature_engineering_predict(n_clicks, selected_duties):
    if n_clicks > 0:
        # Prepare the input data in the format expected by the model
        input_data = {duty: 0 for duty in base_duties}
        for duty in selected_duties:
            input_data[duty] = 1
        
        input_df = pd.DataFrame([input_data])
        
        # Ensure all columns from training data are present in input data (fill missing columns with 0s)
        missing_cols = set(model.feature_names_in_) - set(input_df.columns)
        for col in missing_cols:
            input_df[col] = 0
        # Reorder columns to match the training data
        input_df = input_df[model.feature_names_in_]

        # Make prediction
        prediction = model.predict(input_df)[0]
        return f"Predicted PGTAs Recruited: {prediction}"
    return ""