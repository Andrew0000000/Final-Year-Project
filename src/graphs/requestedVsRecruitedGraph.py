import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, dash_table
import numpy as np
from data_processing.dataProcessing import handle_missing_data, column_sum, difference_calculation, set_color, no_data_modules

filePath_requestedVsRecruited = '../data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = '../data/capVsActualStudentsData.csv'

df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)
df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)

# list modules with 'no data found' in their respective years
noDataModules2122 = no_data_modules(df_requestedVsRecruited, '2021-22 requested', '2021-22 recruited')
noDataModules2223 = no_data_modules(df_requestedVsRecruited, '2022-23 requested', '2022-23 recruited')
noDataModules2324 = no_data_modules(df_requestedVsRecruited, '2023-24 requested', '2023-24 recruited')

# Replace 'No data found' with 0 in the specified columns
columns_to_replace = [
    '2023-24 requested', 
    '2022-23 requested', 
    '2021-22 requested', 
    '2023-24 recruited', 
    '2022-23 recruited', 
    '2021-22 recruited']

handle_missing_data(df_requestedVsRecruited, columns_to_replace)

# statistics of total students and PGTAs
total_recruited_2122 = column_sum(df_requestedVsRecruited, '2021-22 recruited')
total_requested_2122 = column_sum(df_requestedVsRecruited, '2021-22 requested')
total_recruited_2223 = column_sum(df_requestedVsRecruited, '2022-23 recruited')
total_requested_2223 = column_sum(df_requestedVsRecruited, '2022-23 requested')
total_recruited_2324 = column_sum(df_requestedVsRecruited, '2023-24 recruited')
total_requested_2324 = column_sum(df_requestedVsRecruited, '2023-24 requested')
total_students_2223 = column_sum(df_capVsActualStudents, '2022-23 actual students')

stats_layout = html.Div([
    html.Div([
        dcc.Markdown("**Total PGTAs Recruited in 21-22:** " + str(total_recruited_2122)),
        dcc.Markdown("**Total PGTAs Recruited in 22-23:** " + str(total_recruited_2223)),
        dcc.Markdown("**Total PGTAs Recruited in 23-24:** " + str(total_recruited_2324)),
    ], className='stats-column'),
    html.Div([
        dcc.Markdown("**Total PGTAs Requested in 21-22:** " + str(total_requested_2122)),
        dcc.Markdown("**Total PGTAs Requested in 22-23:** " + str(total_requested_2223)),
        dcc.Markdown("**Total PGTAs Requested in 23-24:** " + str(total_requested_2324)),
    ], className='stats-column'),
    html.Div([
        dcc.Markdown("**Total Students in 22-23:** " + str(total_students_2223))
    ])
], className='stats-container')

def requestedVsRecruitedGraphLayout():
    options = [{'label': year, 'value': year} for year in ['2023-24', '2022-23', '2021-22']]
    
    return html.Div([
        dcc.Dropdown(
            options=options,
            value='2023-24',
            id='requestedVsRecruitedGraphDropdown'
        ),
        dcc.Graph(figure={}, id='requestedVsRecruitedGraph'),
        html.Div([
            dcc.Markdown("**No Data Modules in 21-22:** " + ", ".join(noDataModules2122)),
            dcc.Markdown("**No Data Modules in 22-23:** " + ", ".join(noDataModules2223)),
            dcc.Markdown("**No Data Modules in 23-24:** " + ", ".join(noDataModules2324))
        ])
    ])


def requestedVsRecruitedGraph(selected_year):
    difference_calculation(df_requestedVsRecruited, selected_year)
    colors = set_color(df_requestedVsRecruited)

    # plot the bar for pgtas recruited
    trace_recruited = go.Bar(
        x=df_requestedVsRecruited[selected_year + ' recruited'],
        y=df_requestedVsRecruited['Module Code'],
        name='Recruited',
        text=['Diff: ' + str(diff) for diff in df_requestedVsRecruited['Difference']],  
        marker_color=colors,
        orientation='h'
    )
    # plot the bar for pgtas requested
    trace_requested = go.Bar(
        x=df_requestedVsRecruited[selected_year + ' requested'],
        y=df_requestedVsRecruited['Module Code'],
        name='Requested',
        text=['Diff: ' + str(diff) for diff in df_requestedVsRecruited['Difference']],  
        marker_color=colors,
        orientation='h'
    )
    layout = go.Layout(
        title=f'Comparison of Requested vs Recruited PGTAs for {selected_year}',
        barmode='group',
        xaxis_title='Count',
        yaxis_title='Module Code',
        hovermode='closest',
        height=5000,
        width=1700
    )
    return go.Figure(data=[trace_recruited, trace_requested], layout=layout)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Graph with dropdown of modules, showing selected module's history of recruited vs requested
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def moduleHistoryGraphLayout():
    # Get a list of unique modules from the dataframe
    modules = df_requestedVsRecruited['Module Code'].unique().tolist()
    options = [{'label': module, 'value': module} for module in modules]
    
    return html.Div([
        dcc.Dropdown(
            options=options,
            value=modules[0],  # Default value set to the first module in the list
            id='moduleHistoryGraphDropdown'
        ),
        dcc.Graph(figure={}, id='moduleHistoryGraph'),
        # html.Div(id='moduleStudentsDisplay')
    ])

def moduleHistoryGraph(selected_module):
    # Filter the dataframe for the selected module
    module_data = df_requestedVsRecruited[df_requestedVsRecruited['Module Code'] == selected_module]

    traces = []
    for year in ['2021-22', '2022-23', '2023-24']:
        difference_calculation(module_data, year)
        colors = set_color(module_data)

        # Create traces for each year
        trace_recruited = go.Bar(
            x=[year],
            y=[module_data[year + ' recruited'].values[0]],
            name=f'Recruited {year}',
            text=['Diff: ' + str(diff) for diff in df_requestedVsRecruited['Difference']],  
            marker_color=colors.values[0],
        )
        trace_requested = go.Bar(
            x=[year],
            y=[module_data[year + ' requested'].values[0]],
            name=f'Requested {year}',
            text=['Diff: ' + str(diff) for diff in df_requestedVsRecruited['Difference']],  
            marker_color=colors.values[0],
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