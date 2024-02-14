import pytest
import nltk
from nltk.corpus import wordnet
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.data_processing.dataProcessing as dp

def test_no_data_modules():
    data = {'Module Code': ['M1', 'M2', 'M3'], 'col1': ['No data found', 'Data', 'Data'], 'col2': ['Data', 'No data found', 'Data']}
    df = pd.DataFrame(data)
    assert dp.no_data_modules(df, 'col1', 'col2') == ['M1', 'M2']

def test_create_combined_variables_df():
    data1 = {'Module Code': ['M1', 'M2', 'M3'], 'Exam:Coursework Ratio': ['50:50', '60:40', '70:30'], 'Delivery Code': ['DC1', 'DC2', 'DC3']}
    data2 = {'Module Code': ['M1', 'M2', 'M3'], '2022-23 actual students': [100, 200, 300]}
    data3 = {'Module Code': ['M1', 'M2', 'M3'], '2022-23 recruited': [50.0, 100, 150.0]}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    result = dp.create_combined_variables_df(df1, df2, df3)
    assert result['Module Code'].tolist() == ['M1', 'M2', 'M3']
    assert result['Number of Students'].tolist() == [100, 200, 300]
    assert result['Delivery Code'].tolist() == ['DC1', 'DC2', 'DC3']
    assert result['Exam:Coursework Ratio'].tolist() == ['50:50', '60:40', '70:30']
    assert result['PGTAs Recruited'].tolist() == [50, 100, 150]

def test_create_coursework_exam_ratio_column():
    data = {'Module Code': ['M1', 'M1', 'M1', 'M2', 'M2', 'M2', 'M3', 'M4'], 'Assessment Type Name': ['Exam 1', 'Coursework 1.1', 'Coursework 1.2', 'Exam 2.1', 'Exam 2.2', 'Coursework 2.1', 'Exam 3', 'Coursework 4'], 'Assessment Weight': [80, 10, 10, 20, 20, 60, 100, 100]}
    df = pd.DataFrame(data)
    result = dp.create_coursework_exam_ratio_column(df)
    assert result['Exam:Coursework Ratio'].tolist() == ['80:20', '40:60', '100:0', '0:100']

def test_split_coursework_exam_ratio_column():
    data = {'Module Code': ['M1', 'M2', 'M3'], 'Exam:Coursework Ratio': ['50:50', '60:40', '70:30']}
    df = pd.DataFrame(data)
    result = dp.split_coursework_exam_ratio_column(df)
    assert result['Exam Weight'].tolist() == [50, 60, 70]
    assert result['Coursework Weight'].tolist() == [50, 40, 30]

def test_handle_missing_data():
    data = {'col1': ['No data found', 1, 1], 'col2': [1, 'No data found', 1], 'col3': [1, 1, 'No data found']}
    df = pd.DataFrame(data)
    col = ['col1', 'col2', 'col3']
    result = dp.handle_missing_data(df, col)
    assert result['col1'].tolist() == [0, 1, 1]
    assert result['col2'].tolist() == [1, 0, 1]
    assert result['col3'].tolist() == [1, 1, 0]

def test_handle_nan_data():
    data = {'col1': [None, 1, 1], 'col2': [1, None, 1], 'col3': [1, 1, None]}
    df = pd.DataFrame(data)
    result = dp.handle_nan_data(df)
    assert result['col1'].tolist() == [0, 1, 1]
    assert result['col2'].tolist() == [1, 0, 1]
    assert result['col3'].tolist() == [1, 1, 0]

def test_column_sum():
    data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    df = pd.DataFrame(data)
    assert dp.column_sum(df, 'col1') == 6
    assert dp.column_sum(df, 'col2') == 15

def test_column_average():
    data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    df = pd.DataFrame(data)
    assert dp.column_average(df, 'col1') == 2
    assert dp.column_average(df, 'col2') == 5

def test_difference_calculation():
    selected_year = 'year 1'
    data = {'year 1 requested': [4, 5, 6], 'year 1 recruited': [1, 2, 3]}
    df = pd.DataFrame(data)
    df = dp.difference_calculation(df, selected_year)
    assert df['Difference'].tolist() == [3, 3, 3]

def test_set_color():
    data = {'Difference': [3, -3, 3]}
    df = pd.DataFrame(data)
    result = dp.set_color(df)
    assert result.tolist() == ['green', 'red', 'green']

def test_load_data():
    data = {'Number of Students': [100, 200, 300], 'Exam Weight': [40, 50, 60], 'Coursework Weight': [60, 50, 40], 'Delivery Code': ['DC1', 'DC2', 'DC3'], 'PGTAs Recruited': [10, 20, 30]}
    df = pd.DataFrame(data)
    X, y = dp.load_data(df)
    # check if the original Delivery Code column is removed
    assert 'Delivery Code' not in X.columns
    # check if the encoded columns have the correct binary values
    assert (X['Delivery Code_DC1'] == [1, 0, 0]).all()
    assert (X['Delivery Code_DC2'] == [0, 1, 0]).all()
    assert (X['Delivery Code_DC3'] == [0, 0, 1]).all()
    assert X['Number of Students'].tolist() == [100, 200, 300]
    assert X['Exam Weight'].tolist() == [40, 50, 60]
    assert X['Coursework Weight'].tolist() == [60, 50, 40]
    assert y.tolist() == [10, 20, 30]

def test_get_total_pgta_hours():
    data = {'Module Code': ['M1', 'M2', 'M3'], 'PGTA hours excluding marking': [10, 10, 10], 'Marking hours excluding end of year exam (if required)': [10, 10, 20], 'Marking hours for end of year exam (if required)': [10, 10, None]}
    df = pd.DataFrame(data)
    result = dp.get_total_pgta_hours(df)
    assert result['PGTA hours'].tolist() == [30, 30, 30]

def test_split_duties():
    assert dp.split_duties('Duty 1') == ['Duty 1']
    assert dp.split_duties('Duty 1, Duty 2') == ['Duty 1', 'Duty 2']
    assert dp.split_duties('Duty 1, Duty 2 (a, b, c), Duty 3') == ['Duty 1', 'Duty 2 (a, b, c)', 'Duty 3']

def test_get_set_of_duties():
    data1 = {'Duties': ['Duty 1, Duty 2', 'Duty 3', 'Duty 1', 'Duty 2', 'Duty 3']}
    df1 = pd.DataFrame(data1)
    assert dp.get_set_of_duties(df1['Duties']) == {'Duty 1', 'Duty 2', 'Duty 3'}

    data2 = {'Duties': ['Duty 1, Duty 2', 'Duty 3, Duty 4', 'Duty 4, Duty 5']}
    df2 = pd.DataFrame(data2)
    assert dp.get_set_of_duties(df2['Duties']) == {'Duty 1', 'Duty 2', 'Duty 3', 'Duty 4', 'Duty 5'}

def test_create_feature_vector():
    data = {'Duties': ['Duty 1, Duty 2', 'Duty 2, Duty 5', 'Duty 3, Duty 4', 'Duty 4, Duty 5']}
    df = pd.DataFrame(data)
    unique_duties = {'Duty 1', 'Duty 2', 'Duty 3', 'Duty 4', 'Duty 5'}
    result = dp.create_feature_vector(df, unique_duties)
    assert result['Duty 1'].tolist() == [1, 0, 0, 0]
    assert result['Duty 2'].tolist() == [1, 1, 0, 0]
    assert result['Duty 3'].tolist() == [0, 0, 1, 0]
    assert result['Duty 4'].tolist() == [0, 0, 1, 1]
    assert result['Duty 5'].tolist() == [0, 1, 0, 1]

def test_filter_base_duty_in_duties():
    data = {'Duties': ['Duty 1, Duty 2', 'Duty 2, Duty 5', 'Duty 3, Duty 4', 'Duty 4, Duty 5']}
    df = pd.DataFrame(data)

    result1 = dp.filter_base_duty_in_duties(df, 'Duty 4')
    assert result1['Duties'].tolist() == ['Duty 3, Duty 4', 'Duty 4, Duty 5']

    result2 = dp.filter_base_duty_in_duties(df, 'Duty 2')
    assert result2['Duties'].tolist() == ['Duty 1, Duty 2', 'Duty 2, Duty 5']

def test_tokenize_text():
    text = ""
    assert dp.tokenize_text(text) == []

    text = "Dan's car isn't that fast."
    assert dp.tokenize_text(text) == ['Dan', "'s", 'car', 'is', "n't", 'that', 'fast', '.']

    text = "The price is $10.99."
    assert dp.tokenize_text(text) == ['The', 'price', 'is', '$', '10.99', '.']

    text = "Hello. How are you?"
    assert dp.tokenize_text(text) == ['Hello', '.', 'How', 'are', 'you', '?']

    text = "   This    is   a   test.   "
    assert dp.tokenize_text(text) == ['This', 'is', 'a', 'test', '.']

    text = "The long-term goal is to succeed."
    assert dp.tokenize_text(text) == ['The', 'long-term', 'goal', 'is', 'to', 'succeed', '.']

def test_remove_stopwords():
    text = ['This', 'is', 'a', 'sentence']
    assert dp.remove_stopwords(text) == ['This', 'sentence']

    text1 = ['Here', 'are', 'some', 'stopwords', 'in', 'this', 'sentence']
    assert dp.remove_stopwords(text1) == ['Here', 'stopwords', 'sentence']

    text2 = ['There', 'are', 'some', 'stopwords', 'in', 'this', 'long', 'sentence', 'such', 'as', 'and', 'etc.']
    assert dp.remove_stopwords(text2) == ['There', 'stopwords', 'long', 'sentence', 'etc.']

def test_get_wordnet_pos():
    nltk.download('averaged_perceptron_tagger')
    assert dp.get_wordnet_pos('running') == wordnet.VERB
    assert dp.get_wordnet_pos('Beautiful') == wordnet.ADJ
    assert dp.get_wordnet_pos('quickly') == wordnet.ADV
    assert dp.get_wordnet_pos('ideas') == wordnet.NOUN
    assert dp.get_wordnet_pos('Honest') == wordnet.ADJ
    assert dp.get_wordnet_pos('bank') == wordnet.NOUN
    assert dp.get_wordnet_pos('xyz') == wordnet.NOUN

def test_lemmatize_tokens():
    text = ['runs', 'swimming', 'drove']
    text1 = ['jumped', 'walked', 'looked']
    text2 = ['better', 'best', 'good']
    text3 = ['went', 'children', 'teeth']
    
    nltk.download('wordnet')
    assert dp.lemmatize_tokens(text) == ['run', 'swim', 'drove']
    assert dp.lemmatize_tokens(text1) == ['jumped', 'walk', 'look']
    assert dp.lemmatize_tokens(text2) == ['well', 'best', 'good']
    assert dp.lemmatize_tokens(text3) == ['go', 'child', 'teeth']
