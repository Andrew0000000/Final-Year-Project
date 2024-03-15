import os
import sys
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import preprocess_text_list
import numpy as np
from ml_models.modelSaving import save_model

def train_tf_idf_model(df):

    X = df['duties']
    y = df['pgtas_recruited']

    # Preprocess the 'Duties' text data
    X_preprocessed = preprocess_text_list(X)

    # Create a pipeline with TF-IDF Vectorization and Linear Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('regressor', Ridge(alpha=1.0, random_state=42))
    ])

    # Fit the pipeline to the data
    pipeline.fit(X_preprocessed, y)

    kf = KFold(n_splits=3, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X_preprocessed, y, cv=kf, scoring='neg_mean_squared_error')
    rmse_scores = np.sqrt(-scores)

    print("TF-IDF Vectorization Mean RMSE:", rmse_scores.mean())
    print("TF-IDF Vectorization Standard deviation:", rmse_scores.std())

    save_model(pipeline, 'TF-IDF_model.pkl')
    print("TF-IDF Vectorization Model trained and saved as TF-IDF_model.pkl")
