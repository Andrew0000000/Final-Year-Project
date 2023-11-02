import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

df = pd.read_csv('../data/CapAndActualData.csv')
df['Difference'] = df['2023-24 cap'] - df['2022-23 actual students']
colors = df['Difference'].apply(lambda x: 'red' if x < 0 else 'green')

def capAndActualGraph():
    trace1 = go.Bar(
        x=df['Module Code'],
        y=df['2022-23 actual students'],
        name='Actual Students',
        text=df['Difference'],
        marker_color=colors
    )

    trace2 = go.Bar(
        x=df['Module Code'],
        y=df['2023-24 cap'],
        name='Capacity',
        text=df['Difference'],
        marker_color=colors
    )

    # Create the layout
    layout = go.Layout(
        title='Comparison of Capacity vs. Actual Students',
        barmode='group',
        yaxis_title='Count',
        xaxis_title='Module Code',
        hovermode='closest'
    )

    return go.Figure(data=[trace1, trace2], layout=layout)

def capAndActualGraphLayout():
    return html.Div([
        dcc.Graph(figure=capAndActualGraph(), id="capAndActualGraph")
    ])

