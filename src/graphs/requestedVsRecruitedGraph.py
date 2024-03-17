import sys
import os
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataProcessing import difference_calculation, set_colour
from data_processing.statsLayout import stats_layout
from database.models import RequestedVsRecruited


# import data from database
DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(RequestedVsRecruited)
df_requestedVsRecruited = pd.read_sql(query.statement, engine)

def requestedVsRecruitedGraphLayout():
    options = [{'label': year, 'value': year} for year in ['23_24', '22_23', '21_22']]
    
    return html.Div([
        dcc.Dropdown(
            options=options,
            value='23_24',
            id='requestedVsRecruitedGraphDropdown'
        ),
        dcc.Graph(figure={}, id='requestedVsRecruitedGraph'),
        stats_layout,
    ])


def requestedVsRecruitedGraph(selected_year):
    layout = go.Layout(
        title=f'Comparison of Requested vs Recruited PGTAs for {selected_year}',
        barmode='group',
        xaxis_title='Count',
        yaxis_title='Module Code',
        hovermode='closest',
        height=5000,
        width=1700
    )

    df = difference_calculation(df_requestedVsRecruited, selected_year)
    colours = set_colour(df)

    # plot the bar for pgtas recruited
    trace_recruited = go.Bar(
        
        x=df[f'recruited_{selected_year}'],
        y=df['module_code'],
        name='Recruited',
        text=['Diff: ' + str(diff) for diff in df['Difference']],  
        marker_color=colours,
        orientation='h'
    )
    # plot the bar for pgtas requested
    trace_requested = go.Bar(
        x=df[f'requested_{selected_year}'],
        y=df['module_code'],
        name='Requested',
        text=['Diff: ' + str(diff) for diff in df['Difference']],  
        marker_color=colours,
        orientation='h'
    )
    return go.Figure(data=[trace_recruited, trace_requested], layout=layout)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Graph with dropdown of modules, showing selected module's history of recruited vs requested
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def moduleHistoryGraphLayout():
    # Get a list of unique modules from the dataframe
    modules = df_requestedVsRecruited['module_code'].unique().tolist()
    options = [{'label': module, 'value': module} for module in modules]
    
    return html.Div([
        dcc.Dropdown(
            options=options,
            value=modules[0],  # Default value set to the first module in the list
            id='moduleHistoryGraphDropdown'
        ),
        dcc.Graph(figure={}, id='moduleHistoryGraph'),
        stats_layout,
        # html.Div(id='moduleStudentsDisplay')
    ])

def moduleHistoryGraph(selected_module):
    # Filter the dataframe for the selected module
    module_data = df_requestedVsRecruited[df_requestedVsRecruited['module_code'] == selected_module]

    traces = []
    for year in ['21_22', '22_23', '23_24']:
        # Create traces for each year
        df = difference_calculation(df_requestedVsRecruited, year)
        colours = set_colour(df)

        trace_recruited = go.Bar(
            x=[year],
            y=[module_data[f'recruited_{year}'].values[0]],
            name=f'Recruited {year}',
            text=['Diff: ' + str(diff) for diff in df['Difference']],  
            marker_color=colours,
        )
        trace_requested = go.Bar(
            x=[year],
            y=[module_data[f'requested_{year}'].values[0]],
            name=f'Requested {year}',
            text=['Diff: ' + str(diff) for diff in df['Difference']],  
            marker_color=colours,
        )
        traces.extend([trace_recruited, trace_requested])

    layout = go.Layout(
        title=f'Comparison of Requested vs Recruited PGTAs for {selected_module}',
        barmode='group',
        xaxis_title='Year',
        yaxis_title='Count',
        hovermode='closest',
        height=700,
        width=1200
    )
    return go.Figure(data=traces, layout=layout)

session.close()
