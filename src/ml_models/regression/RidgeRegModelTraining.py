import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import one_hot_encode_delivery_code
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Ridge
import numpy as np
from ml_models.modelSaving import save_model

def train_ridge_regression_model(df):
    # Prepare the features and target variables
    df = one_hot_encode_delivery_code(df)

    X = df[['number_of_students', 'exam_weight', 'coursework_weight', 'delivery_code_A4U', 'delivery_code_A5U', 'delivery_code_A6U', 'delivery_code_A7U', 'delivery_code_A7P']]
    y = df['pgtas_recruited']

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
