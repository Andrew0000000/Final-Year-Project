import numpy as np
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pygam import LinearGAM, s, f
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_processing.dataProcessing import one_hot_encode_delivery_code
from ml_models.modelSaving import save_model

def train_generalised_additive_model(df):
    # Prepare the features and target variables
    df = one_hot_encode_delivery_code(df)

    X = df[['number_of_students', 'exam_weight', 'coursework_weight', 'delivery_code_A4U', 'delivery_code_A5U', 'delivery_code_A6U', 'delivery_code_A7U', 'delivery_code_A7P']]
    y = df['pgtas_recruited']

    # Setting up the GAM model with spline terms for continuous features and factor terms for categorical
    terms = s(0) + s(1) + s(2) # Spline terms for the continuous features
    for i in range(3, X.shape[1]):  # f() for encoded categorical features starting from index 3 onwards
        terms += f(i)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    gam = LinearGAM(terms)
    gam.fit(X_train, y_train)

    y_pred = gam.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("Generalised Additive Model RMSE:", rmse)

    # Save the trained model
    save_model(gam, 'gam_model.pkl')
    print("Generalised Additive Model trained and saved as gam_model.pkl")
    print('---------------------------------------------------------------------------------')
