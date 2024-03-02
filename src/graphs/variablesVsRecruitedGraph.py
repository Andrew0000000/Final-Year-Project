import sys
import os
import pandas as pd
import plotly.express as px
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataframeCleaning import df_combined_data
from database.models import CombinedData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# import data from database
DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(CombinedData)
df_combined_data = pd.read_sql(query.statement, engine)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def studentsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=studentsVsRecruitedGraph(), id='studentsVsRecruitedGraph')
    ])

def studentsVsRecruitedGraph():
    fig = px.scatter(
        df_combined_data,
        x='number_of_students',
        y='pgtas_recruited',
        hover_name='module_code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def examWeightsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=examWeightsVsRecruitedGraph(), id='examWeightsVsRecruitedGraph')
    ])

def examWeightsVsRecruitedGraph():
    fig = px.scatter(
        df_combined_data,
        x='exam_coursework_ratio',
        y='pgtas_recruited',
        hover_name='module_code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def deliveryCodeVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=deliveryCodeVsRecruitedGraph(), id='deliveryCodeVsRecruitedGraph')
    ])

def deliveryCodeVsRecruitedGraph():
    fig = px.scatter(
        df_combined_data,
        x='delivery_code',
        y='pgtas_recruited',
        hover_name='module_code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
