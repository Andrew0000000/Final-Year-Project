import pandas as pd
from dash import html, dcc
from models.modelLoading import load_model
import os 
from data_processing.dataProcessing import get_set_of_duties, preprocess_text


project_base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
filePath_jobDescriptionData = os.path.join(project_base_path, 'data/jobDescriptionData.csv')
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
base_duties = get_set_of_duties(df_jobDescriptionData['Duties'])

# load the feature engineering model
model_type = 'TF-IDF'
model = load_model(f'{model_type}_model.pkl')

def vectoriserPredictorLayout():
    return html.Div([
        html.H1("PGTAs Recruitment Predictor with TF-IDF Vectoriser"),

        # create radio items for each base duty
        html.Div([
            dcc.Checklist(
                id='base-duties-checklist',
                options=[{'label': duty, 'value': duty} for duty in base_duties],
                value=[],
                labelStyle={'display': 'block'}
            ),
        ]),
        html.Br(),
        html.Button('Predict', id='vectoriser-prediction-button', n_clicks=0),
        html.Hr(),
        html.Br(),
        html.Div(id='vectoriser-prediction-output')
    ])

def vectoriserPredictor(n_clicks, selected_duties):
    if n_clicks > 0:
        # take the selected duties, join them together by a comma and feed into the model
        input_data = ', '.join(selected_duties)
        preprocessed_input_data = preprocess_text(input_data)
        prediction = model.predict([preprocessed_input_data])[0]
        return f"Predicted PGTAs Recruited: {prediction}"
    return ""