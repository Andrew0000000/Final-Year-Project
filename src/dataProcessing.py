import pandas as pd
import numpy as np


# Define a new DataFrame consisting of the following data: Module Code, Number of Students, PGTAs Recruited, Exam:Coursework Ratio, Delivery Code
def create_combined_variables_df(df_moduleAssessmentData, df_capVsActualStudents, df_requestedVsRecruited):
    combined_data_list = []
    # Assuming 'Number of Students' is a column in df_capVsActualStudents
    for module in df_moduleAssessmentData['Module Code'].unique():
        # the module code column in df_moduleAssessmentData and df_requestedVsRecruited are different. Only take the pgta data if the module from
        # df_requestedVsRecruited exists in df_moduleAssessmentData
        if module in df_capVsActualStudents['Module Code'].values and module in df_requestedVsRecruited['Module Code'].values:

            # extract data from thier respective dataframes
            students_2324 = df_capVsActualStudents[df_capVsActualStudents['Module Code'] == module]['2022-23 actual students'].iloc[0]
            recruited_2324 = df_requestedVsRecruited[df_requestedVsRecruited['Module Code'] == module]['2023-24 recruited'].iloc[0]
            exam_coursework_ratio = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module]['Exam:Coursework Ratio'].iloc[0]
            delivery_code = df_moduleAssessmentData[df_moduleAssessmentData['Module Code'] == module]['Delivery Code'].iloc[0]

            row_data = {
                'Module Code': module,
                'Number of Students': students_2324,
                'PGTAs Recruited': recruited_2324,
                'Exam:Coursework Ratio': exam_coursework_ratio,
                'Delivery Code': delivery_code
            }

            combined_data_list.append(row_data)

    combined_data_list = sorted(combined_data_list, key=lambda d: d['Exam:Coursework Ratio'],  reverse=True)
    # converts list into dataframe
    combined_data = pd.DataFrame(combined_data_list)

    # replace 'No data found' values with 0 to prevent complexities in plotting
    combined_data['PGTAs Recruited'] = combined_data['PGTAs Recruited'].drop(1).reset_index(drop=True).replace('No data found', 0).apply(pd.to_numeric, errors='coerce')

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

# Replace 'No data found' with 0 in the specified columns
def handle_missing_data(df, columns):
    for col in columns:
        df[col] = df[col].replace('No data found', 0)
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
    return columns

def column_sum(df, column):
    return df[column].sum()

# calculate the difference between pgtas requested and recruited
def difference_calculation(df, selected_year):
    df['Difference'] = df[selected_year + ' requested'] - df[selected_year + ' recruited']
    return df

# red is shown for PGTAs recruited > requested, signalling demand higher than expected
def set_color(df):
    return df['Difference'].apply(lambda x: 'red' if x < 0 else 'green')
    