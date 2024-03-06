import os
import sys
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from data_processing.dataProcessing import download_nltk_resources, get_set_of_duties, create_feature_vector
import numpy as np
from ml_models.modelSaving import save_model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import JobDescription
from data_processing.dataframeCleaning import duties


# import the data from the database
DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(JobDescription)
df_jobDescriptionData = pd.read_sql(query.statement, engine)

download_nltk_resources()

X = df_jobDescriptionData[duties]
y = df_jobDescriptionData['total_hours']

# Initialize and train the RandomForestRegressor
model = RandomForestRegressor(random_state=42)
model = model.fit(X, y)

# Evaluate the model
kf = KFold(n_splits=3, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-scores)

print("RMSE scores for each fold:", rmse_scores)
print("Mean RMSE:", rmse_scores.mean())
print("Standard deviation:", rmse_scores.std())

save_model(model, 'feature_engineering_model.pkl')
print("Model trained and saved as feature_engineering_model.pkl")

session.close()