from dash import html, dcc
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from data_processing.dataframeCleaning import duties
import dash_bootstrap_components as dbc
import pandas as pd


DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()
meta.reflect(bind=engine)
table_names = list(meta.tables.keys())
inspector = inspect(engine)
table_names = inspector.get_table_names()



def tableLayout():
    return dbc.Container([
        dbc.Tabs(
            id="db-tabs",
            children=[dbc.Tab(
                label=table_name, 
                tab_id=table_name
            ) for table_name in table_names],
            active_tab=table_names[0] if table_names else None,
        ),
        html.Div(id="table-content")
    ], fluid=True)

def display_table(active_tab):
    if active_tab is None:
        return "No table selected"
    
    # Query the database for the selected table
    df = pd.read_sql_table(active_tab, con=engine)
    
    # Create the table header
    table_header = [
        html.Thead(html.Tr([html.Th(col) for col in df.columns]))
    ]
    
    # Create the table body
    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ]
    
    # Combine header and body in a dbc.Table
    table = dbc.Table(table_header + table_body, bordered=True, dark=True, hover=True, responsive=True, striped=True)
    
    return table
