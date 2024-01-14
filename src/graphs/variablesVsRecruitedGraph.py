import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table
from data_processing.dataProcessing import create_coursework_exam_ratio_column, create_combined_variables_df

filePath_requestedVsRecruited = '../data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = '../data/capVsActualStudentsData.csv'
filePath_moduleAssessmentData = '../data/moduleAssessmentData.csv'

#  Data from df_moduleAssessmentData is edited as follows:
#   - duplicated data is removed (exact same data for all columns)
#   - there are many modules with different variants eg. COMP0025 with delivery codes A6U, A7U, A7P. Only one type of delivery code is retained
#     to prevent duplicates in the graphs

df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)
df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)
df_moduleAssessmentData = pd.read_csv(filePath_moduleAssessmentData)


df_moduleAssessmentData = create_coursework_exam_ratio_column(df_moduleAssessmentData)
combined_data = create_combined_variables_df(df_moduleAssessmentData, df_capVsActualStudents, df_requestedVsRecruited)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def studentsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=studentsVsRecruitedGraph(), id='studentsVsRecruitedGraph')
    ])

def studentsVsRecruitedGraph():
    fig = px.scatter(
        combined_data,
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
        combined_data,
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
        combined_data,
        x='Delivery Code',
        y='PGTAs Recruited',
        hover_name='Module Code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
