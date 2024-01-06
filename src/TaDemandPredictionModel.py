import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataProcessing import create_combined_variables_df, create_coursework_exam_ratio_column, split_coursework_exam_ratio_column
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
import numpy as np

filePath_requestedVsRecruited = 'data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = 'data/capVsActualStudentsData.csv'
filePath_moduleAssessmentData = 'data/moduleAssessmentData.csv'


df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)
df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)
df_moduleAssessmentData = pd.read_csv(filePath_moduleAssessmentData)

df_moduleAssessmentData = create_coursework_exam_ratio_column(df_moduleAssessmentData)
combined_data = create_combined_variables_df(df_moduleAssessmentData, df_capVsActualStudents, df_requestedVsRecruited)

print(combined_data.head())

combined_data = split_coursework_exam_ratio_column(combined_data)

print(combined_data.head())

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

# One-hot encode categorical features
categorical_features = ['Delivery Code']
numeric_features = ['Number of Students', 'Exam Weight', 'Coursework Weight']


module_code = list(combined_data['Module Code'])
number_of_students = list(combined_data['Number of Students'])
exam_weight = list(combined_data['Exam Weight'])
coursework_weight = list(combined_data['Coursework Weight'])
delivery_code = list(combined_data['Delivery Code'])

print(module_code)
print(number_of_students)
print(exam_weight)
print(coursework_weight)
print(delivery_code)


# For demonstration, let's use the previously defined data
df = pd.DataFrame({
    'Module Code': ['COMP0009', 'COMP0002', 'COMP0004', 'COMP0024', 'COMP0068'],
    'Number of Students': [169, 170, 171, 97, 70],
    'PGTAs Recruited': [199.0, 166.0, 0.0, 5.0, 32.0],
    'Delivery Code': ['A5U', 'A4U', 'A4U', 'A6U', 'A7P'],
    'Exam Weight': [95, 90, 90, 90, 90],
    'Coursework Weight': [5, 10, 10, 10, 10]
})

# Convert categorical data to numerical values using one-hot encoding
df_encoded = pd.get_dummies(df, columns=['Module Code', 'Delivery Code'])

# Define features and target
X = df_encoded.drop('PGTAs Recruited', axis=1)
y = df_encoded['PGTAs Recruited']

# Initialize the cross-validation method
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Perform cross-validation
cv_scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')

# Convert MSE to RMSE and print results
rmse_scores = np.sqrt(-cv_scores)
print('RMSE scores for each fold:', rmse_scores)
print('Mean RMSE:', np.mean(rmse_scores))
