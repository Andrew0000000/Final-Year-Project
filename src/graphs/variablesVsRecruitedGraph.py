import sys
import os
import pandas as pd
import plotly.express as px
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataframeCleaning import df_combined_data


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def studentsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=studentsVsRecruitedGraph(), id='studentsVsRecruitedGraph')
    ])

def studentsVsRecruitedGraph():
    fig = px.scatter(
        df_combined_data,
        x='Number of Students',
        y='PGTAs Recruited',
        hover_name='Module Code',
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
        x='Exam:Coursework Ratio',
        y='PGTAs Recruited',
        hover_name='Module Code',
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
        x='Delivery Code',
        y='PGTAs Recruited',
        hover_name='Module Code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
