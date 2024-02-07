import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_processing.dataProcessing import no_data_modules, create_combined_variables_df, handle_missing_data

def test_no_data_modules():
    data = {'Module Code': ['M1', 'M2', 'M3'], 'col1': ['No data found', 'Data', 'Data'], 'col2': ['Data', 'No data found', 'Data']}
    df = pd.DataFrame(data)
    assert no_data_modules(df, 'col1', 'col2') == ['M1', 'M2']

def test_create_combined_variables_df():
    data1 = {'Module Code': ['M1', 'M2', 'M3'], 'Exam:Coursework Ratio': [0.5, 0.6, 0.7], 'Delivery Code': ['DC1', 'DC2', 'DC3']}
    data2 = {'Module Code': ['M1', 'M2', 'M3'], '2022-23 actual students': [100, 200, 300]}
    data3 = {'Module Code': ['M1', 'M2', 'M3'], '2022-23 recruited': [50, 100, 150]}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    result = create_combined_variables_df(df1, df2, df3)
    assert result['Module Code'].tolist() == ['M3', 'M2', 'M1']
    assert result['Number of Students'].tolist() == [300, 200, 100]
    assert result['PGTAs Recruited'].tolist() == [150, 100, 50]
    assert result['Exam:Coursework Ratio'].tolist() == [0.7, 0.6, 0.5]
    assert result['Delivery Code'].tolist() == ['DC3', 'DC2', 'DC1']

def test_handle_missing_data():
    data = {'col1': ['No data found', 'Data', 1], 'col2': ['Data', 'No data found', 2], 'col3': [3, 'No data found', 'Data']}
    df = pd.DataFrame(data)
    result = handle_missing_data(df, ['col1', 'col2'])
    assert result['col1'].tolist() == [0, 'Data', 1]
    assert result['col2'].tolist() == ['Data', 0, 2]
    assert result['col3'].tolist() == [3, 'No data found', 'Data']
