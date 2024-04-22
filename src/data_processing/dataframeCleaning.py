import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing import dataProcessing


filePath_jobDescriptionData = '../data/jobDescriptionData.csv'
filePath_requestedVsRecruited = '../data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = '../data/capVsActualStudentsData.csv'
filePath_moduleAssessmentData = '../data/moduleAssessmentData.csv'

df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)
df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)
df_moduleAssessmentData = pd.read_csv(filePath_moduleAssessmentData)

#  Data from df_moduleAssessmentData is manually edited as follows:
#   - duplicated data is removed (exact same data for all columns)
#   - there are many modules with different variants eg. COMP0025 with delivery codes A6U, A7U, A7P. Only one type of delivery code is retained
#     to prevent duplicates in the graphs

columns_to_replace = [
    '2023-24 requested', 
    '2022-23 requested', 
    '2021-22 requested', 
    '2023-24 recruited', 
    '2022-23 recruited', 
    '2021-22 recruited'
]

df_moduleAssessmentDataCleaned = dataProcessing.create_coursework_exam_ratio_column(df_moduleAssessmentData)

df_jobDescriptionDataCleaned = dataProcessing.get_total_pgta_hours(df_jobDescriptionData)
df_jobDescriptionDataCleaned = dataProcessing.split_module_code_and_name(df_jobDescriptionDataCleaned)

duties = list(dataProcessing.get_set_of_duties(df_jobDescriptionDataCleaned['duties']))

df_requestedVsRecruitedCleaned = dataProcessing.handle_missing_data(df_requestedVsRecruited, columns_to_replace)

df_capVsActualStudentsCleaned = df_capVsActualStudents

df_combined_variables = dataProcessing.create_combined_variables_df(df_moduleAssessmentDataCleaned, df_capVsActualStudentsCleaned, df_requestedVsRecruitedCleaned, df_jobDescriptionDataCleaned)

df_averagePGTAHours = dataProcessing.create_df_average_pgta_hours(df_jobDescriptionDataCleaned, duties)



# Print functions for debugging
# # print the number of rows in the df
# print(f"Number of rows in df_jobDescriptionDataCleaned: {len(df_jobDescriptionDataCleaned)}")
# print(f"Number of rows in df_requestedVsRecruitedCleaned: {len(df_requestedVsRecruitedCleaned)}")
# print(f"Number of rows in df_capVsActualStudentsCleaned: {len(df_capVsActualStudentsCleaned)}")
# print(f"Number of rows in df_moduleAssessmentDataCleaned: {len(df_moduleAssessmentDataCleaned)}")
# print(f"Number of rows in df_combined_variables: {len(df_combined_variables)}")
# print(f"Number of rows in df_averagePGTAHours: {len(df_averagePGTAHours)}")

# # print number of columns in the df
# print(f"Number of columns in df_jobDescriptionDataCleaned: {len(df_jobDescriptionDataCleaned.columns)}")
# print(f"Number of columns in df_requestedVsRecruitedCleaned: {len(df_requestedVsRecruitedCleaned.columns)}")
# print(f"Number of columns in df_capVsActualStudentsCleaned: {len(df_capVsActualStudentsCleaned.columns)}")
# print(f"Number of columns in df_moduleAssessmentDataCleaned: {len(df_moduleAssessmentDataCleaned.columns)}")
# print(f"Number of columns in df_combined_variables: {len(df_combined_variables.columns)}")
# print(f"Number of columns in df_averagePGTAHours: {len(df_averagePGTAHours.columns)}")
