import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataProcessing import create_combined_variables_df, create_coursework_exam_ratio_column, split_coursework_exam_ratio_column, handle_nan_data, load_data
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import numpy as np


def linear_regression(X, y):
    return RandomForestRegressor(n_estimators=100, random_state=42)

def ridge_regression(X, y):
    return Ridge(alpha=1.0, random_state=42)


filePath_requestedVsRecruited = 'data/requestedVsRecruitedData.csv'
filePath_capVsActualStudents = 'data/capVsActualStudentsData.csv'
filePath_moduleAssessmentData = 'data/moduleAssessmentData.csv'


df_capVsActualStudents = pd.read_csv(filePath_capVsActualStudents)
df_requestedVsRecruited = pd.read_csv(filePath_requestedVsRecruited)
df_moduleAssessmentData = pd.read_csv(filePath_moduleAssessmentData)

df_moduleAssessmentData = create_coursework_exam_ratio_column(df_moduleAssessmentData)
df = create_combined_variables_df(df_moduleAssessmentData, df_capVsActualStudents, df_requestedVsRecruited)
df = split_coursework_exam_ratio_column(df)
df = handle_nan_data(df)

module_code = list(df['Module Code'])
number_of_students = list(df['Number of Students'])
exam_weight = list(df['Exam Weight'])
coursework_weight = list(df['Coursework Weight'])
delivery_code = list(df['Delivery Code'])


# Prepare the features and target variables
X, y = load_data(df)


# Convert categorical data to dummy variables
X = pd.get_dummies(X)

model_type = 'ridge'

# Initialize the K-Fold cross-validator
kf = KFold(n_splits=20, shuffle=True, random_state=42)


# Initialize the model based on flag
if model_type == 'ridge':
    model = ridge_regression(X, y)
else:
    model = linear_regression(X, y)

# Perform cross-validation and compute the scores
scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')

# Convert the scores to root mean squared error (RMSE)
rmse_scores = np.sqrt(-scores)

# Print the RMSE for each fold
print("RMSE scores for each fold:", rmse_scores)

# Print the mean RMSE
print("Mean RMSE:", rmse_scores.mean())
