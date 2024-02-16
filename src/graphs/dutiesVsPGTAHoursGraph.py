import sys
import os
import pandas as pd
import plotly.express as px
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataProcessing import get_total_pgta_hours, get_set_of_duties, column_average, filter_base_duty_in_duties

filePath_jobDescriptionData = '../data/jobDescriptionData.csv'
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
df_jobDescriptionData = get_total_pgta_hours(df_jobDescriptionData)

duties = list(get_set_of_duties(df_jobDescriptionData['Duties']))

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
        x='Select module',
        y='PGTA hours',
        title=f'PGTA Hours for Duty: {duty}'
    )
    max_hours = df_jobDescriptionData['PGTA hours'].max()
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
    df_averagePGTAHours = pd.DataFrame()
    df_averagePGTAHours['Duty'] = duties
    average_pgta_hours = []
    for duty in duties:
        average_pgta_hours.append(column_average(filter_base_duty_in_duties(df_jobDescriptionData, duty), 'PGTA hours'))
    df_averagePGTAHours['Average PGTA Hours'] = average_pgta_hours
    fig = px.bar(
        df_averagePGTAHours,
        x='Duty',
        y='Average PGTA Hours',
        title='Average PGTA Hours for Each Duty',
        height=1100
    )
    return fig
