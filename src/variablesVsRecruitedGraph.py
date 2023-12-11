import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table

filePath_requestedVsRecruited = '../data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = '../data/capVsActualStudentsData.csv'
filePath_moduleAssessmentData = '../data/moduleAssessmentData.csv'

#  Data from df_moduleAssessmentData is edited as follows:
#   - duplicated data is removed (exact same data for all columns)
#   - there are many modules with different variants eg. COMP0025 with delivery codes A6U, A7U, A7P. Only one type of delivery code is retained
#     to prevent duplicates in the graphs

df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)
df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)
df_moduleAssessmentData = pd.read_csv(filePath_moduleAssessmentData)


# group weightage of exams and courseworks for each module
exam_type_assessment = df_moduleAssessmentData[df_moduleAssessmentData['Assessment Type Name'].str.contains('Exam')]
coursework_type_assessment = df_moduleAssessmentData[~df_moduleAssessmentData['Assessment Type Name'].str.contains('Exam')]
total_exam_weights = exam_type_assessment.groupby('Module Code')['Assessment Weight'].sum().reset_index()
total_coursework_weights = coursework_type_assessment.groupby('Module Code')['Assessment Weight'].sum().reset_index()

# merge the exam and coursework weights above into the dataframe and create the Exam:Coursework Ratio column
df_moduleAssessmentData = df_moduleAssessmentData.drop_duplicates(subset='Module Code')
df_moduleAssessmentData = df_moduleAssessmentData.merge(total_exam_weights, on='Module Code', how='left')
df_moduleAssessmentData = df_moduleAssessmentData.merge(total_coursework_weights, on='Module Code', how='left')
df_moduleAssessmentData['Assessment Weight_y'].fillna(0, inplace=True)
df_moduleAssessmentData['Assessment Weight'].fillna(0, inplace=True)
df_moduleAssessmentData['Exam:Coursework Ratio'] = df_moduleAssessmentData.apply(lambda row: f"{int(row['Assessment Weight_y'])}:{int(row['Assessment Weight'])}", axis=1)


# Define the structure of the new DataFrame
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

print(combined_data.head(10))



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def studentsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=studentsVsRecruitedGraph(), id='studentsVsRecruitedGraph')
    ])

def studentsVsRecruitedGraph():
    fig = px.scatter(
        combined_data,
        x='Number of Students',
        y='PGTAs Recruited',
        hover_name='Module Code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def examWeightsVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=examWeightsVsRecruitedGraph(), id='examWeightsVsRecruitedGraph')
    ])

def examWeightsVsRecruitedGraph():
    fig = px.scatter(
        combined_data,
        x='Exam:Coursework Ratio',
        y='PGTAs Recruited',
        hover_name='Module Code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def deliveryCodeVsRecruitedGraphLayout():
    return html.Div([
        dcc.Graph(figure=deliveryCodeVsRecruitedGraph(), id='deliveryCodeVsRecruitedGraph')
    ])

def deliveryCodeVsRecruitedGraph():
    fig = px.scatter(
        combined_data,
        x='Delivery Code',
        y='PGTAs Recruited',
        hover_name='Module Code',
    )
    fig.update_traces(textposition='top center')

    return fig

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
