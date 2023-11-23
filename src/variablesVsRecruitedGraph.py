import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table

filePath_requestedVsRecruited = '../data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = '../data/capVsActualStudentsData.csv'

df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)
df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)

modules = df_requestedVsRecruited['Module Code'].unique().tolist()
students = df_capVsActualStudents['2022-23 actual students']
# remove the duplicated data of pgta recruited for comp0002
PGTAs_recruited = df_requestedVsRecruited['2022-23 recruited'].drop(1).reset_index(drop=True)

df_studentsVsRecruited = pd.DataFrame()
df_studentsVsRecruited['Module Code'] = modules
df_studentsVsRecruited['students'] = students
df_studentsVsRecruited['PGTAs recruited'] = PGTAs_recruited
print(df_studentsVsRecruited.head())
def studentsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=studentsVsRecruitedGraph(), id='studentsVsRecruitedGraph')
    ])


def studentsVsRecruitedGraph():

    fig = px.scatter(
        df_studentsVsRecruited,
        x='students',
        y='PGTAs recruited',
        hover_name='Module Code',
    )
    fig.update_traces(textposition='top center')

    return fig
