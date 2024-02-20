import os
import sys
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import download_nltk_resources, get_set_of_duties, get_total_pgta_hours, create_feature_vector
import numpy as np
from models.modelSaving import save_model

# Download NLTK resources
download_nltk_resources()

filePath_jobDescriptionData = '../data/jobDescriptionData.csv'

# Load the data
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
df_jobDescriptionData = get_total_pgta_hours(df_jobDescriptionData)
unique_duties = list(get_set_of_duties(df_jobDescriptionData['Duties']))
df_jobDescriptionData = create_feature_vector(df_jobDescriptionData, unique_duties)

X = df_jobDescriptionData[unique_duties]
y = df_jobDescriptionData['PGTA hours']

# Initialize and train the RandomForestRegressor
model = RandomForestRegressor(random_state=42)
model = model.fit(X, y)

# Evaluate the model
kf = KFold(n_splits=3, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-scores)

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())

save_model(model, 'feature_engineering_model.pkl')
print("Model trained and saved as feature_engineering_model.pkl")