import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, dash_table
import numpy as np

filePath = '../data/requestedVsRecruitedData.csv'

df = pd.read_csv(filePath)

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

def requestedVsRecruitedGraphLayout():
    options = [{'label': year, 'value': year} for year in ['2023-24', '2022-23', '2021-22']]
    columns_to_display = [{'name': col, 'id': col} for col in df.columns if col not in ['Module Code and Title']]
    
    return html.Div([
        dcc.Dropdown(
            options=options,
            value='2023-24',
            id='requestedVsRecruitedGraphDropdown'
        ),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=columns_to_display,
            page_size=10
        ),
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
    trace1 = go.Bar(
        x=df[selected_year + ' recruited'],
        y=df['Module Code'],
        name='Recruited',
        text=df['Difference'],
        marker_color=colors,
        orientation='h'
    )
    # plot the bar for pgtas requested
    trace2 = go.Bar(
        x=df[selected_year + ' requested'],
        y=df['Module Code'],
        name='Requested',
        text=df['Difference'],
        marker_color=colors,
        orientation='h'
    )
    layout = go.Layout(
        title='Comparison of Requested vs. Recruited Students',
        barmode='group',
        xaxis_title='Count',
        yaxis_title='Module Code',
        hovermode='closest',
        height=5000,  # Adjust the height as needed
        width=1800  # Adjust the width as needed
    )
    return go.Figure(data=[trace1, trace2], layout=layout)
