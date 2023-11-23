import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, dash_table
import numpy as np

filePath_requestedVsRecruited = '../data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = '../data/capVsActualStudentsData.csv'

df = pd.read_csv(filePath_requestedVsRecruited)
df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)

# list modules with 'no data found' in their respective years
noDataModules2122 = df.loc[
    (df['2021-22 requested'] == 'No data found') | 
    (df['2021-22 recruited'] == 'No data found'),
    'Module Code'].tolist()
noDataModules2223 = df.loc[
    (df['2022-23 requested'] == 'No data found') | 
    (df['2022-23 recruited'] == 'No data found'),
    'Module Code'].tolist()
noDataModules2324 = df.loc[
    (df['2023-24 requested'] == 'No data found') | 
    (df['2023-24 recruited'] == 'No data found'),
    'Module Code'].tolist()

# Replace 'No data found' with 0 in the specified columns
columns_to_replace = [
    '2023-24 requested', 
    '2022-23 requested', 
    '2021-22 requested', 
    '2023-24 recruited', 
    '2022-23 recruited', 
    '2021-22 recruited']

for col in columns_to_replace:
    df[col] = df[col].replace('No data found', 0)
df[columns_to_replace] = df[columns_to_replace].apply(pd.to_numeric, errors='coerce')


# statistics of total students and PGTAs
total_recruited_2122 = df['2021-22 recruited'].sum()
total_requested_2122 = df['2021-22 requested'].sum()
total_recruited_2223 = df['2022-23 recruited'].sum()
total_requested_2223 = df['2022-23 requested'].sum()
total_recruited_2324 = df['2023-24 recruited'].sum()
total_requested_2324 = df['2023-24 requested'].sum()
total_students_2223 = df_capVsActualStudents['2022-23 actual students'].sum() 

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
        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=columns_to_display,
        #     page_size=10
        # ),
        dcc.Graph(figure={}, id='requestedVsRecruitedGraph'),
        html.Div([
            dcc.Markdown("**No Data Modules in 21-22:** " + ", ".join(noDataModules2122)),
            dcc.Markdown("**No Data Modules in 22-23:** " + ", ".join(noDataModules2223)),
            dcc.Markdown("**No Data Modules in 23-24:** " + ", ".join(noDataModules2324))
        ])
    ])

def requestedVsRecruitedGraph(selected_year):
    # calculate the difference between pgtas requested and recruited
    df['Difference'] = df[selected_year + ' requested'] - df[selected_year + ' recruited']
    # red is shown for pgtas recruited > requested, signalling demand higher than expected
    colors = df['Difference'].apply(lambda x: 'red' if x < 0 else 'green')

    # plot the bar for pgtas recruited
    trace_recruited = go.Bar(
        x=df[selected_year + ' recruited'],
        y=df['Module Code'],
        name='Recruited',
        text=['Diff: ' + str(diff) for diff in df['Difference']],  
        marker_color=colors,
        orientation='h'
    )
    # plot the bar for pgtas requested
    trace_requested = go.Bar(
        x=df[selected_year + ' requested'],
        y=df['Module Code'],
        name='Requested',
        text=['Diff: ' + str(diff) for diff in df['Difference']],  
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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  Graph with dropdown of modules, showing selected module's history of recruited vs requested
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def moduleHistoryGraphLayout():
    # Get a list of unique modules from the dataframe
    modules = df['Module Code'].unique().tolist()
    options = [{'label': module, 'value': module} for module in modules]
    
    return html.Div([
        dcc.Dropdown(
            options=options,
            value=modules[0],  # Default value set to the first module in the list
            id='moduleHistoryGraphDropdown'
        ),
        # dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[{'name': col, 'id': col} for col in df.columns if col not in ['Module Code and Title']],
        #     page_size=10
        # ),
        dcc.Graph(figure={}, id='moduleHistoryGraph')
    ])

def moduleHistoryGraph(selected_module):
    # Filter the dataframe for the selected module
    module_data = df[df['Module Code'] == selected_module]

    traces = []
    for year in ['2021-22', '2022-23', '2023-24']:
        # Calculate the difference for each year
        module_data['Difference'] = module_data[year + ' requested'] - module_data[year + ' recruited']
        colors = module_data['Difference'].apply(lambda x: 'red' if x < 0 else 'green')

        # Create traces for each year
        trace_recruited = go.Bar(
            x=[year],
            y=[module_data[year + ' recruited'].values[0]],
            name=f'Recruited {year}',
            text=['Diff: ' + str(diff) for diff in df['Difference']],  
            marker_color=colors.values[0],
        )
        trace_requested = go.Bar(
            x=[year],
            y=[module_data[year + ' requested'].values[0]],
            name=f'Requested {year}',
            text=['Diff: ' + str(diff) for diff in df['Difference']],  
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