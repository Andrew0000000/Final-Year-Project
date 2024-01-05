import pandas as pd


filePath_moduleAssessmentData = '../data/moduleAssessmentData.csv'
df_moduleAssessmentData = pd.read_csv(filePath_moduleAssessmentData)

modules = df_moduleAssessmentData['Assessment Type Name'].unique().tolist()

print(modules)
print(len(modules))

weights = ['Exam (In Person Written) (Centrally Managed)', 
            'Coursework', 
            'Group project', 
            'Exam (Remote Online) (Centrally Managed)', 
            'Department test', 
            'Group coursework', 
            'Practical examination (Departmentally managed)', 
            'Report', 
            'Study abroad', 
            'Take-Home Paper 48 Hours (Departmentally Managed)', 
            'Oral examination (Departmentally managed)', 
            'Take-Home Paper 72 Hours (Departmentally Managed)']




