import os
import sys
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import Ridge
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import numpy as np
from ml_models.modelSaving import save_model
from data_processing.dataProcessing import create_feature_vector

def train_feature_engineering_model(df, duties):
    df = create_feature_vector(df, duties)
    X = df[duties]
    y = df['pgtas_recruited']

    model = Ridge(alpha=1.0, random_state=42)
    model = model.fit(X, y)

    # Evaluate the model
    kf = KFold(n_splits=3, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
    rmse_scores = np.sqrt(-scores)

    print("Feature Engineering Mean RMSE:", rmse_scores.mean())
    print("Feature Engineering Standard deviation:", rmse_scores.std())

    save_model(model, 'feature_engineering_model.pkl')
    print("Feature Engineering Model trained and saved as feature_engineering_model.pkl")
