import pandas as pd
import numpy as np
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pygam import LinearGAM, s, f
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataProcessing import load_regession_data

def train_generalised_additive_model(df):
    # Prepare the features and target variables
    X, y = load_regession_data(df)
    
    # Setting up the GAM model with spline terms for continuous features and factor terms for categorical
    terms = s(0) + s(1) + s(2) # Spline terms for the continuous features
    for i in range(3, X.shape[1]):  # f() for encoded categorical features starting from index 3 onwards
        terms += f(i)

    gam = LinearGAM(terms)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    gam.fit(X_train, y_train)

    y_pred = gam.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("Generalised Additive Model RMSE:", rmse)
    print('---------------------------------------------------------------------------------')
