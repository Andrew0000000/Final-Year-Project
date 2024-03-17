import pandas as pd
import re
from sklearn.preprocessing import OneHotEncoder
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# =======================================================================
# HANDLES DATA PROCESSING FOR GRAPH PLOTTING AND LINEAR REGRESSION MODELS
# =======================================================================

# list modules with 'no data found' in their respective years
def no_data_modules(df, col1, col2):
    return df.loc[(df[col1] == 'No data found') | (df[col2] == 'No data found'), 'Module Code'].tolist()

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
    df['Difference'] = df[f'requested_{selected_year}'] - df[f'recruited_{selected_year}']
    return df

# red is shown for PGTAs recruited > requested, signalling demand higher than expected
def set_colour(df):
    colours = []
    for diff in df['Difference']:
        if diff < 0:
            colours.append('red')
        else:
            colours.append('green')
    return colours

def load_regession_data(df):
    X = df[['number_of_students', 'exam_weight', 'coursework_weight', 'delivery_code']]
    y = df['pgtas_recruited']

    # One-hot encode the 'delivery_code' column
    encoder = OneHotEncoder(sparse=False)
    encoded_delivery_code = encoder.fit_transform(X[['delivery_code']])
    
    # Create a DataFrame from the encoded array
    encoded_delivery_code_df = pd.DataFrame(encoded_delivery_code, columns=encoder.get_feature_names_out(['delivery_code']))

    # Drop the original 'Delivery Code' column and concatenate the encoded columns
    X = X.drop('delivery_code', axis=1)
    X = pd.concat([X, encoded_delivery_code_df], axis=1)
    return X, y


# ==============================================
# HANDLES DATA PROCESSING FOR DATAFRAME CLEANING
# ==============================================

# Obtain the total PGTA hours needed including marking
def get_total_pgta_hours(df):
    df = handle_nan_data(df)
    df['PGTA hours'] = df['PGTA hours excluding marking'] + df['Marking hours excluding end of year exam (if required)'] + df['Marking hours for end of year exam (if required)']
    df = df.drop(['PGTA hours excluding marking', 'Marking hours excluding end of year exam (if required)', 
                  'Marking hours for end of year exam (if required)', 'Timestamp', 
                  'Enter text to be used in the advert for your module', 'Select up to 3 categories that best fit the role',
                  'When is the module taught/delivered?'
                  ], axis=1)
    return df

def split_module_code_and_name(df):
    # splits module code and name into two separate columns
    df.rename(columns={'Select module': 'Module Code'}, inplace=True)
    df['Module Name'] = df['Module Code'].apply(lambda x: (' ').join(x.split(' ')[1:]))
    df['Module Code'] = df['Module Code'].apply(lambda x: x.split(' ')[0])
    return df

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
    df.rename(columns={'Assessment Weight_y':'Exam Weight', 'Assessment Weight':'Coursework Weight'}, inplace=True)
    df['Exam Weight'].fillna(0, inplace=True)
    df['Coursework Weight'].fillna(0, inplace=True)
    df['Exam:Coursework Ratio'] = df.apply(lambda row: f"{int(row['Exam Weight'])}:{int(row['Coursework Weight'])}", axis=1)
    df = df.drop(['Assessment Weight_x', 'Assessment Sequence Number', 'Assessment Type Name', 'Assessment Title', 'Assessment Type Code'], axis=1)

    return df

# Define a new DataFrame consisting of the following data: Module Code, Number of Students, PGTAs Recruited, Exam:Coursework Ratio, Delivery Code, PGTA Hours and Duties
def create_combined_variables_df(df_moduleAssessmentData, df_capVsActualStudents, df_requestedVsRecruited, df_jobDescriptionData):
    combined_data_list = []
    
    for module_code in df_jobDescriptionData['Module Code'].unique():

        # the module code column in df_moduleAssessmentData and df_requestedVsRecruited are different. Only take the pgta data if the module from
        # df_requestedVsRecruited exists in df_moduleAssessmentData
        if module_code in df_capVsActualStudents['Module Code'].values and module_code in df_requestedVsRecruited['Module Code'].values and module_code in df_moduleAssessmentData['Module Code'].values:
            # extract data from their respective dataframes
            module_name = df_jobDescriptionData[df_jobDescriptionData['Module Code'] == module_code]['Module Name'].iloc[0]
            students_2223 = df_capVsActualStudents[df_capVsActualStudents['Module Code'] == module_code]['2022-23 actual students'].iloc[0]
            recruited_2223 = df_requestedVsRecruited[df_requestedVsRecruited['Module Code'] == module_code]['2022-23 recruited'].iloc[0]
            exam_coursework_ratio = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module_code]['Exam:Coursework Ratio'].iloc[0]
            exam_weight = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module_code]['Exam Weight'].iloc[0]
            coursework_weight = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module_code]['Coursework Weight'].iloc[0]
            delivery_code = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module_code]['Delivery Code'].iloc[0]
            duties = df_jobDescriptionData[df_jobDescriptionData['Module Code'] == module_code]['duties'].iloc[0]

            row_data = {
                'Module Code': module_code,
                'Module Name': module_name,
                'Number of Students': students_2223,
                'PGTAs Recruited': recruited_2223,
                'Exam:Coursework Ratio': exam_coursework_ratio,
                'Exam Weight': exam_weight,
                'Coursework Weight': coursework_weight,
                'Delivery Code': delivery_code,
                'Duties': duties
            }

            combined_data_list.append(row_data)

    # converts list into dataframe
    df_combined = pd.DataFrame(combined_data_list)

    # replace 'No data found' values with 0 to prevent complexities in plotting
    df_combined = handle_nan_data(df_combined)

    return df_combined

def create_df_average_pgta_hours(df, duties):
    df_averagePGTAHours = pd.DataFrame()
    df_averagePGTAHours['duties'] = duties
    average_pgta_hours = []
    for duty in duties:
        average_pgta_hours.append(column_average(filter_base_duty_in_duties(df, duty), 'PGTA hours'))
    df_averagePGTAHours['Average PGTA Hours'] = average_pgta_hours
    return df_averagePGTAHours

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

def create_feature_vector(df, unique_duties):
    for duty in unique_duties:
        df[duty] = 0
    for index, row in df.iterrows():
        for duty in unique_duties:
            if duty in row['duties']:
                df.at[index, duty] = 1
    return df

def filter_base_duty_in_duties(df, duty):
    return df[df['duties'].str.contains(re.escape(duty), case=False, na=False)]


# ==========================
# HANDLES TEXT PREPROCESSING
# ==========================

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
def preprocess_text(text):
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return ' '.join(lemmatized_tokens)

# Preprocess all descriptions in a list and return a transformed list
def preprocess_text_list(text_list):
    return text_list.apply(preprocess_text)
