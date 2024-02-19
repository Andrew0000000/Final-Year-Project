import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import create_combined_variables_df, create_coursework_exam_ratio_column, split_coursework_exam_ratio_column, handle_nan_data, load_data
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from models.modelSaving import save_model

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

# Prepare the features and target variables
X, y = load_data(df)

# Convert categorical data to dummy variables
X = pd.get_dummies(X)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Initialize the K-Fold cross-validator
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Perform cross-validation and compute the scores
scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')

# Convert the scores to root mean squared error (RMSE)
rmse_scores = np.sqrt(-scores)

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())

# Save the trained model
save_model(model, 'linear_model.pkl')
print("Model trained and saved as linear_model.pkl")
