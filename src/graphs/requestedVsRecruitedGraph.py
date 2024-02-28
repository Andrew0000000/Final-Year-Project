import sys
import os
import plotly.graph_objects as go
from dash import html, dcc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataProcessing import difference_calculation, set_color
from data_processing.dataframeCleaning import df_requestedVsRecruitedCleaned
from data_processing.statsLayout import stats_layout, noDataModules2122, noDataModules2223, noDataModules2324, noDataModules2122, noDataModules2223, noDataModules2324

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
            'Empty rows represent data that is not available in the dataset'
        ]),
        html.Div([
            html.Div([
                dcc.Markdown("**No Data Modules in 21-22:** " + ", ".join(noDataModules2122)),
                dcc.Markdown("**No Data Modules in 22-23:** " + ", ".join(noDataModules2223)),
                dcc.Markdown("**No Data Modules in 23-24:** " + ", ".join(noDataModules2324)),
            ], className='stats-column'),
        ], className='stats-container'),
        stats_layout,
    ])


def requestedVsRecruitedGraph(selected_year):
    difference_calculation(df_requestedVsRecruitedCleaned, selected_year)
    colors = set_color(df_requestedVsRecruitedCleaned)

    # plot the bar for pgtas recruited
    trace_recruited = go.Bar(
        x=df_requestedVsRecruitedCleaned[selected_year + ' recruited'],
        y=df_requestedVsRecruitedCleaned['Module Code'],
        name='Recruited',
        text=['Diff: ' + str(diff) for diff in df_requestedVsRecruitedCleaned['Difference']],  
        marker_color=colors,
        orientation='h'
    )
    # plot the bar for pgtas requested
    trace_requested = go.Bar(
        x=df_requestedVsRecruitedCleaned[selected_year + ' requested'],
        y=df_requestedVsRecruitedCleaned['Module Code'],
        name='Requested',
        text=['Diff: ' + str(diff) for diff in df_requestedVsRecruitedCleaned['Difference']],  
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
    modules = df_requestedVsRecruitedCleaned['Module Code'].unique().tolist()
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
    module_data = df_requestedVsRecruitedCleaned[df_requestedVsRecruitedCleaned['Module Code'] == selected_module]

    traces = []
    for year in ['2021-22', '2022-23', '2023-24']:
        difference_calculation(module_data, year)
        colors = set_color(module_data)

        # Create traces for each year
        trace_recruited = go.Bar(
            x=[year],
            y=[module_data[year + ' recruited'].values[0]],
            name=f'Recruited {year}',
            text=['Diff: ' + str(diff) for diff in df_requestedVsRecruitedCleaned['Difference']],  
            marker_color=colors.values[0],
        )
        trace_requested = go.Bar(
            x=[year],
            y=[module_data[year + ' requested'].values[0]],
            name=f'Requested {year}',
            text=['Diff: ' + str(diff) for diff in df_requestedVsRecruitedCleaned['Difference']],  
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