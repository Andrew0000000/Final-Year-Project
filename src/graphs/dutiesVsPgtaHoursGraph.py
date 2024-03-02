import sys
import os
import pandas as pd
import plotly.express as px
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataProcessing import filter_base_duty_in_duties
from data_processing.dataframeCleaning import duties
from database.models import JobDescription, AveragePGTAHours
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import data from database 
DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
query_JobDescription = session.query(JobDescription)
query_AveragePGTAHours = session.query(AveragePGTAHours)
df_jobDescriptionData = pd.read_sql(query_JobDescription.statement, engine)
df_averagePGTAHours = pd.read_sql(query_AveragePGTAHours.statement, engine)

# plot the graph of duties vs pgta hours where duty in duties is present in the dataframe
def dutiesVsPGTAHoursGraphLayout():
    return html.Div([
        dcc.Dropdown(
            id='dutiesVsPGTAHoursGraphDropdown',
            options=[{'label': duty, 'value': duty} for duty in duties],
            value=duties[0]
        ),
        dcc.Graph(figure=dutiesVsPGTAHoursGraph(duties[0]), id='dutiesVsPGTAHoursGraph'),
    ])

def dutiesVsPGTAHoursGraph(duty):
    df = filter_base_duty_in_duties(df_jobDescriptionData, duty)
    fig = px.bar(
        df, 
        x='module_code',
        y='total_hours',
        title=f'PGTA Hours for Duty: {duty}'
    )
    max_hours = df_jobDescriptionData['total_hours'].max()
    min_hours = 0
    fig.update_layout(
        yaxis=dict(
            range=[min_hours, max_hours + 10]  # Adding a buffer to the maximum for better visualization
        ),
        height=1100
    )
    return fig

# plot another graph showing the average pgta hours for each duty
def dutiesVsPGTAHoursAverageGraphLayout():
    return html.Div([
        dcc.Graph(figure=dutiesVsPGTAHoursAverageGraph(), id='dutiesVsPGTAHoursAverageGraph'),
    ])

def dutiesVsPGTAHoursAverageGraph():
    fig = px.bar(
        df_averagePGTAHours,
        x='duties',
        y='average_hours',
        title='Average PGTA Hours for Each Duty',
        height=1100
    )
    return fig

session.close()