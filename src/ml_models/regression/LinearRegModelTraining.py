import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import load_regession_data
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from ml_models.modelSaving import save_model

def train_linear_regression_model(df):
    # Prepare the features and target variables
    X, y = load_regession_data(df)

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

    print("Linear Regression Mean RMSE:", rmse_scores.mean())
    print("Linear Regression Standard deviation:", rmse_scores.std())

    # Save the trained model
    save_model(model, 'linear_model.pkl')
    print("Linear Regression Model trained and saved as linear_model.pkl")