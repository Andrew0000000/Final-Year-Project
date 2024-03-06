import os
import sys
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import download_nltk_resources, preprocess_text_list
import numpy as np
from ml_models.modelSaving import save_model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import JobDescription

# import the data from the database
DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(JobDescription)
df_jobDescriptionData = pd.read_sql(query.statement, engine)

download_nltk_resources()

X = df_jobDescriptionData['duties']
y = df_jobDescriptionData['total_hours']

# Preprocess the 'Duties' text data
X_preprocessed = preprocess_text_list(X)

# Create a pipeline with TF-IDF Vectorization and Linear Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('regressor', RandomForestRegressor())
])

# Fit the pipeline to the data
pipeline.fit(X_preprocessed, y)

kf = KFold(n_splits=3, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X_preprocessed, y, cv=kf, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-scores)

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())

save_model(pipeline, 'TF-IDF_model.pkl')
print("Model trained and saved as TF-IDF_model.pkl")

session.close()