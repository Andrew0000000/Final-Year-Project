import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataProcessing import create_combined_variables_df, create_coursework_exam_ratio_column, split_coursework_exam_ratio_column, handle_nan_data, load_data
import numpy as np
from pygam import LinearGAM, s
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


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

print(df.head())

# Prepare the features and target variables
X, y = load_data(df)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Assuming you have your training data in X_train and y_train
gam = LinearGAM(s(0, penalties='auto') + s(1, penalties='auto') + s(2, penalties='auto') + s(3, penalties='auto') + s(4, penalties='auto'))
gam.fit(X_train, y_train)
y_pred = gam.predict(X_test)


print("RMSE:", mean_squared_error(y_test, y_pred, squared=False))