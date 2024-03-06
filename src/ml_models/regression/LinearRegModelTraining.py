import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import create_combined_variables_df, create_coursework_exam_ratio_column, split_coursework_exam_ratio_column, handle_nan_data, load_data
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from ml_models.modelSaving import save_model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import CombinedVariables

# import the data from the database
DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(CombinedVariables)
df = pd.read_sql(query.statement, engine)

# Prepare the features and target variables
X, y = load_data(df)

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

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())

# Save the trained model
save_model(model, 'linear_model.pkl')
print("Model trained and saved as linear_model.pkl")

session.close()