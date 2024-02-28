from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
from models import YourModel
from dotenv import load_dotenv
from pandas import pd

load_dotenv()
DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
print(DATABASE_URI)
engine.connect()

Session = sessionmaker(bind=engine)

def import_csv_to_db(csv_file_path, Base, model_class, database_uri):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Convert columns to the correct datatype if necessary
    # For example, converting timestamps:
    # df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M')

    # Create an engine and bind the session to it
    engine = create_engine(database_uri)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Iterate over the DataFrame and create a model instance for each row
    for index, row in df.iterrows():
        model_instance = model_class()
        for column in row.index:
            # Check if the model has an attribute with the same name as the column
            if hasattr(model_instance, column):
                # Set the attribute of the model instance to the value from the row
                setattr(model_instance, column, row[column])

        # Add the model instance to the session
        session.add(model_instance)

    # Commit the session to write the objects to the database
    session.commit()


Base.metadata.create_all(engine)
import_csv_to_db(df_jobDescriptionDataCleaned, database_uri)
print("Data imported to database")