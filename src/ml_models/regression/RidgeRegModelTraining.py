import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import load_regession_data
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Ridge
import numpy as np
from ml_models.modelSaving import save_model

def train_ridge_regression_model(df):
    # Prepare the features and target variables
    X, y = load_regession_data(df)

    # Convert categorical data to dummy variables
    X = pd.get_dummies(X)

    # Train the model
    model = Ridge(alpha=1.0, random_state=42)
    model.fit(X, y)


    # Initialize the K-Fold cross-validator
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Perform cross-validation and compute the scores
    scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')

    # Convert the scores to root mean squared error (RMSE)
    rmse_scores = np.sqrt(-scores)

    print("Ridge Regression Mean RMSE:", rmse_scores.mean())
    print("Ridge Regression Standard deviation:", rmse_scores.std())

    # Save the trained model
    save_model(model, 'ridge_model.pkl')
    print("Ridge Regression Model trained and saved as ridge_model.pkl")
    print('---------------------------------------------------------------------------------')
