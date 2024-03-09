from dash import html, dcc
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataframeCleaning import duties
import dash_bootstrap_components as dbc
import pandas as pd
from database.models import CombinedVariables
from data_processing.dataframeCleaning import duties

DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()
meta.reflect(bind=engine)
table_names = list(meta.tables.keys())
inspector = inspect(engine)
table_names = inspector.get_table_names()



def displayTableLayout():
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

def displayTable(active_tab):
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

def insertModuleLayout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Input(id="module-code-insert", type="text", placeholder="Module Code"),
                html.Br(),
                dbc.Input(id="module-name-insert", type="text", placeholder="Module Name"),
                html.Br(),
                dbc.Input(id="number-of-students-insert", type="text", placeholder="Number of Students"),
                html.Br(),
                dbc.Input(id="pgtas-recruited-insert", type="number", placeholder="PGTAs Recruited"),
                html.Br(),
                dbc.Input(id="exam-weight-insert", type="number", placeholder="Exam Weight"),
                html.Br(),
                dbc.Input(id="coursework-weight-insert", type="number", placeholder="Coursework Weight"),
                html.Br(),
                dbc.Input(id="delivery-code-insert", type="text", placeholder="Delivery Code"),
                html.Br(),
                html.Div("Select duties", style={"font-weight": "bold"}),
                dbc.Checklist(
                    id="base-duties-checklist-insert",
                    value=[],
                    options=[{'label': duty, 'value': duty} for duty in duties],
                ),
                html.Br(),
                dbc.Button("Insert Module", id="insert-module-button", color="primary"),
                html.Br(),
            ], width=6),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id="insert-module-alert")
            ], width=4)
        ])
    ], fluid=True)

def insertModule(n_clicks, module_code, module_name, number_of_students, pgtas_recruited, exam_weight, coursework_weight, delivery_code, duties):
    if n_clicks is not None and n_clicks > 0:
        # Insert data into database
        new_module = CombinedVariables(
            module_code=module_code,
            module_name=module_name,
            number_of_students=number_of_students,
            pgtas_recruited=pgtas_recruited,
            exam_weight=exam_weight,
            coursework_weight=coursework_weight,
            exam_coursework_ratio=f'{exam_weight}:{coursework_weight}',
            delivery_code=delivery_code,
            duties=(', ').join(duties),
        )
        session.add(new_module)
        session.commit()
        session.close()
        return dbc.Alert("Module successfully inserted!", color="success", duration=4000)
    return ""

def deleteModuleLayout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Input(id="module-code-delete", type="text", placeholder="Module Code"),
                html.Br(),
                dbc.Button("Delete Module", id="delete-module-button", color="danger")
            ], width=6)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id="delete-module-alert")
            ], width=4)
        ])
    ], fluid=True)

def deleteModule(n_clicks, moduleCode):
    if n_clicks is not None and n_clicks > 0:
        # Delete data from database
        session = Session()
        # session.query(CombinedVariables).filter(CombinedVariables.module_code == moduleCode).delete()
        # handle module not found
        module = session.query(CombinedVariables).filter(CombinedVariables.module_code == moduleCode).first()
        if not module:
            return dbc.Alert("Module not found!", color="danger")
        session.delete(module)
        session.commit()
        session.close()
        return dbc.Alert("Module successfully deleted!", color="success", duration=4000)
    return ""