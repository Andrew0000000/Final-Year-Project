import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from dataPreprocessing import download_nltk_resources, preprocess_description_list
import numpy as np

# Download NLTK resources
download_nltk_resources()

project_base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))
filePath_jobDescriptionData = os.path.join(project_base_path, 'data/jobDescriptionData.csv')

# Load the data
df_jobDescriptionData = pd.read_csv(filePath_jobDescriptionData)

# Assume 'Duties' column exists and we're predicting 'PGTA hours excluding marking'
X = df_jobDescriptionData['Duties']
y = df_jobDescriptionData['PGTA hours excluding marking']

# Preprocess the 'Duties' text data
X_preprocessed = preprocess_description_list(X)

# Create a pipeline with TF-IDF Vectorization and Linear Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('regressor', LinearRegression())
])

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X_preprocessed, y, cv=kf, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-scores)

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())


for a in df_jobDescriptionData['Duties'].unique():
    print('=========================================')
    print(a)
    print('=========================================')