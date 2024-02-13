import pandas as pd
import re
from sklearn.preprocessing import OneHotEncoder
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# =======================================================================
# HANDLES DATA PROCESSING FOR GRAPH PLOTTING AND LINEAR REGRESSION MODELS
# =======================================================================

# list modules with 'no data found' in their respective years
def no_data_modules(df, col1, col2):
    return df.loc[(df[col1] == 'No data found') | (df[col2] == 'No data found'), 'Module Code'].tolist()

# Define a new DataFrame consisting of the following data: Module Code, Number of Students, PGTAs Recruited, Exam:Coursework Ratio, Delivery Code
def create_combined_variables_df(df_moduleAssessmentData, df_capVsActualStudents, df_requestedVsRecruited):
    combined_data_list = []
    # Assuming 'Number of Students' is a column in df_capVsActualStudents
    for module in df_moduleAssessmentData['Module Code'].unique():
        # the module code column in df_moduleAssessmentData and df_requestedVsRecruited are different. Only take the pgta data if the module from
        # df_requestedVsRecruited exists in df_moduleAssessmentData
        if module in df_capVsActualStudents['Module Code'].values and module in df_requestedVsRecruited['Module Code'].values:

            # extract data from thier respective dataframes
            students_2223 = df_capVsActualStudents[df_capVsActualStudents['Module Code'] == module]['2022-23 actual students'].iloc[0]
            recruited_2223 = df_requestedVsRecruited[df_requestedVsRecruited['Module Code'] == module]['2022-23 recruited'].iloc[0]
            exam_coursework_ratio = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module]['Exam:Coursework Ratio'].iloc[0]
            delivery_code = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module]['Delivery Code'].iloc[0]

            row_data = {
                'Module Code': module,
                'Number of Students': students_2223,
                'PGTAs Recruited': recruited_2223,
                'Exam:Coursework Ratio': exam_coursework_ratio,
                'Delivery Code': delivery_code
            }

            combined_data_list.append(row_data)

    # combined_data_list = sorted(combined_data_list, key=lambda d: d['Exam:Coursework Ratio'],  reverse=True)
    # converts list into dataframe
    combined_data = pd.DataFrame(combined_data_list)

    # replace 'No data found' values with 0 to prevent complexities in plotting and removes the first row as it is the same module as the second row
    combined_data['PGTAs Recruited'] = combined_data['PGTAs Recruited'].reset_index(drop=True).replace('No data found', 0).apply(pd.to_numeric, errors='coerce')

    return combined_data


def create_coursework_exam_ratio_column(df):
    # group weightage of exams and courseworks for each module
    exam_type_assessment = df[df['Assessment Type Name'].str.contains('Exam')]
    coursework_type_assessment = df[~df['Assessment Type Name'].str.contains('Exam')]
    total_exam_weights = exam_type_assessment.groupby('Module Code')['Assessment Weight'].sum().reset_index()
    total_coursework_weights = coursework_type_assessment.groupby('Module Code')['Assessment Weight'].sum().reset_index()

    # merge the exam and coursework weights above into the dataframe and create the Exam:Coursework Ratio column
    df = df.drop_duplicates(subset='Module Code')
    df = df.merge(total_exam_weights, on='Module Code', how='left')
    df = df.merge(total_coursework_weights, on='Module Code', how='left')
    df['Assessment Weight_y'].fillna(0, inplace=True)
    df['Assessment Weight'].fillna(0, inplace=True)
    df['Exam:Coursework Ratio'] = df.apply(lambda row: f"{int(row['Assessment Weight_y'])}:{int(row['Assessment Weight'])}", axis=1)

    return df

def split_coursework_exam_ratio_column(df):
    df[['Exam Weight', 'Coursework Weight']] = df['Exam:Coursework Ratio'].str.split(':', expand=True).astype(int)
    return df.drop('Exam:Coursework Ratio', axis=1)

# Replace 'No data found' with 0 in the specified columns
def handle_missing_data(df, columns):
    for col in columns:
        df[col] = df[col].replace('No data found', 0)
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
    return df

def handle_nan_data(df):
    return df.fillna(0)

# get the sum of the column
def column_sum(df, column):
    return df[column].sum()

# get the average of the column
def column_average(df, column):
    return df[column].mean()

# calculate the difference between pgtas requested and recruited
def difference_calculation(df, selected_year):
    df['Difference'] = df[selected_year + ' requested'] - df[selected_year + ' recruited']
    return df

# red is shown for PGTAs recruited > requested, signalling demand higher than expected
def set_color(df):
    return df['Difference'].apply(lambda x: 'red' if x < 0 else 'green')

def load_data(df):
    X = df[['Number of Students', 'Exam Weight', 'Coursework Weight', 'Delivery Code']]
    y = df['PGTAs Recruited']

    # One-hot encode the 'Delivery Code' column
    encoder = OneHotEncoder(sparse=False)
    encoded_delivery_code = encoder.fit_transform(X[['Delivery Code']])
    
    # Create a DataFrame from the encoded array
    encoded_delivery_code_df = pd.DataFrame(encoded_delivery_code, columns=encoder.get_feature_names_out(['Delivery Code']))

    # Drop the original 'Delivery Code' column and concatenate the encoded columns
    X = X.drop('Delivery Code', axis=1)
    X = pd.concat([X, encoded_delivery_code_df], axis=1)
    return X, y



# =======================================================
# HANDLES DATA PROCESSING FOR NATURAL LANGUAGE PROCESSING
# =======================================================

# Obtain the total PGTA hours needed including marking
def get_total_pgta_hours(df):
    df = handle_nan_data(df)
    df['PGTA hours'] = df['PGTA hours excluding marking'] + df['Marking hours excluding end of year exam (if required)'] + df['Marking hours for end of year exam (if required)']
    return df

# Split the duties into a list of individual duties
def split_duties(duty):
    if duty == 'No data found' or len(duty) == 0:
        return []
    result = []
    stack = []
    temp = ''
    for c in duty:
        if c == '(':
            stack.append(c)
        if c == ')':
            stack.pop()
        if c == ',' and stack == []:
            if temp[0] == ' ' and temp[-1] == ' ':
                result.append(temp[1:-1])
            elif temp[0] == ' ':
                result.append(temp[1:])
            elif temp[-1] == ' ':
                result.append(temp[:-1])
            else:
                result.append(temp)
            temp = ''
        else:
            temp += c
    if temp[0] == ' ' and temp[-1] == ' ':
        result.append(temp[1:-1])
    elif temp[0] == ' ':
        result.append(temp[1:])
    elif temp[-1] == ' ':
        result.append(temp[:-1])
    else:
        result.append(temp)
    return result

# Obtain the set of base duties from the job description
def get_set_of_duties(job_desc):
    base_duties = []
    for duties_combination in job_desc:
        duty = split_duties(duties_combination)
        for d in duty:
            base_duties.append(d)
    return set(base_duties)

def filter_base_duty_in_duties(df, duty):
    return df[df['Duties'].str.contains(re.escape(duty), case=False, na=False, regex=True)]

# Ensure necessary NLTK resources are downloaded
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

# Tokenize the text
def tokenize_text(text):
    return word_tokenize(text)

# Remove stopwords from a list of tokens
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

# Mapping from POS tag to wordnet tag
def get_wordnet_pos(word):
    """Map POS tag to the format accepted by WordNetLemmatizer"""
    pos_tag = nltk.pos_tag([word])[0][1]  # Get the POS tag for the word

    # Define a mapping from the POS tag to the format accepted by WordNetLemmatizer
    tag_dict = {
        'NN': wordnet.NOUN, 'NNS': wordnet.NOUN, 'NNP': wordnet.NOUN, 'NNPS': wordnet.NOUN,
        'VB': wordnet.VERB, 'VBD': wordnet.VERB, 'VBG': wordnet.VERB, 'VBN': wordnet.VERB, 'VBP': wordnet.VERB, 'VBZ': wordnet.VERB,
        'JJ': wordnet.ADJ, 'JJR': wordnet.ADJ, 'JJS': wordnet.ADJ,
        'RB': wordnet.ADV, 'RBR': wordnet.ADV, 'RBS': wordnet.ADV
    }
    return tag_dict.get(pos_tag, wordnet.NOUN)  # Default to NOUN if not found

# Lemmatize a list of tokens
def lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    return  [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens]

# Preprocess a single description
def preprocess_description(text):
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return ' '.join(lemmatized_tokens)

# Preprocess all descriptions in a list and return a transformed list
def preprocess_description_list(description_list):
    return description_list.apply(preprocess_description)

# Vectorize a series of preprocessed documents
def vectorize_documents(preprocessed_text):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(preprocessed_text)


# FEATURE ENGINEERING

def keyword_binary_features(df, keyword):
    # Binary feature for the presence of a specific keyword
    feature_name = f'has_{keyword}'
    df[feature_name] = df['Duties'].str.contains(keyword).astype(int)
    return df

def count_feature(df, phrase):
    # Count occurrences of a specific phrase
    feature_name = f'count_{phrase}'
    df[feature_name] = df['Duties'].str.count(phrase)
    return df

def text_length_feature(df):
    # Text length of the job description
    df['desc_length'] = df['Duties'].str.len()
    return df

download_nltk_resources()