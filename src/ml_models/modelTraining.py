from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from database.models import CombinedVariables
from ml_models.natural_language_processing.featureEngModelTraining import train_feature_engineering_model
from ml_models.natural_language_processing.TF_IDFModelTraining import train_tf_idf_model
from ml_models.regression.LinearRegModelTraining import train_linear_regression_model
from ml_models.regression.RidgeRegModelTraining import train_ridge_regression_model
from ml_models.generalised_additive_model.generalisedAdditiveModel import train_generalised_additive_model
from data_processing.dataProcessing import download_nltk_resources
from data_processing.dataframeCleaning import duties


def modelTrainingLayout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Button("Train Models", id="modelTraining-button")
            ], width=6)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id="modelTraining-alert")
            ], width=4)
        ])
    ], fluid=True)

def modelTraining(n_clicks):
    if n_clicks and n_clicks > 0:
        # import the data from the database
        DATABASE_URI = 'sqlite:///app_database.db'
        engine = create_engine(DATABASE_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(CombinedVariables)
        df = pd.read_sql(query.statement, engine)

        download_nltk_resources()
        # Train the models
        train_generalised_additive_model(df)
        train_linear_regression_model(df)
        train_ridge_regression_model(df)
        train_feature_engineering_model(df, duties)
        train_tf_idf_model(df)

        session.close()
        return dbc.Alert("Models Trained!", color="success", duration=4000)
    return ""
