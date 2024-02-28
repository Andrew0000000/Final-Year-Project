import pandas as pd
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

df_jobDescriptionDataCleaned = dataProcessing.get_total_pgta_hours(df_jobDescriptionData)

df_requestedVsRecruitedCleaned = dataProcessing.handle_missing_data(df_requestedVsRecruited, columns_to_replace)

df_capVsActualStudentsCleaned = df_capVsActualStudents

df_moduleAssessmentDataCleaned = dataProcessing.create_coursework_exam_ratio_column(df_moduleAssessmentData)

df_combined_data = dataProcessing.create_combined_variables_df(df_moduleAssessmentDataCleaned, df_capVsActualStudentsCleaned, df_requestedVsRecruitedCleaned)

duties = list(dataProcessing.get_set_of_duties(df_jobDescriptionDataCleaned['Duties']))
df_averagePGTAHours = dataProcessing.create_df_average_pgta_hours(df_jobDescriptionDataCleaned, duties)