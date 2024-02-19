import os
import sys
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import download_nltk_resources, preprocess_text_list, get_set_of_duties, get_total_pgta_hours, create_feature_vector
import numpy as np
from models.modelSaving import save_model

# Download NLTK resources
download_nltk_resources()

filePath_jobDescriptionData = 'data/jobDescriptionData.csv'

# Load the data
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)
df_jobDescriptionData = get_total_pgta_hours(df_jobDescriptionData)

# Assume 'Duties' column exists and we're predicting 'PGTA hours excluding marking'
X = df_jobDescriptionData['Duties']
y = df_jobDescriptionData['PGTA hours']

# Preprocess the 'Duties' text data
X_preprocessed = preprocess_text_list(X)

# Create a pipeline with TF-IDF Vectorization and Linear Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('regressor', RandomForestRegressor())
])

kf = KFold(n_splits=3, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X_preprocessed, y, cv=kf, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-scores)

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())

save_model(pipeline, 'TF-IDF_model.pkl')
print("Model trained and saved as TF-IDF_model.pkl")