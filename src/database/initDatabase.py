from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import Base, JobDescription, RequestedVsRecruited, CapVsActualStudents, ModuleAssessment, CombinedVariables, AveragePGTAHours
from data_processing.dataframeCleaning import df_jobDescriptionDataCleaned, df_requestedVsRecruitedCleaned, df_capVsActualStudentsCleaned, df_moduleAssessmentDataCleaned, df_combined_variables, df_averagePGTAHours

DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def load_csv_to_database(df, model, session):

    # Get the column names from the model
    model_columns = model.__table__.columns.keys()

    # Iterate over the DataFrame
    for index, row in df.iterrows():
        # Create a dictionary that maps model attributes to CSV column values based on order
        data = {model_columns[index+1]: row[index] for index in range(len(row))}
        
        # Create an instance of the model with the mapped data
        model_instance = model(**data)
        session.add(model_instance)
    
    # Commit the session to save the objects to the database
    session.commit()

def init_db():
    Base.metadata.create_all(engine)
    session = Session()
    load_csv_to_database(df_jobDescriptionDataCleaned, JobDescription, session)
    load_csv_to_database(df_requestedVsRecruitedCleaned, RequestedVsRecruited, session)
    load_csv_to_database(df_capVsActualStudentsCleaned, CapVsActualStudents, session)
    load_csv_to_database(df_moduleAssessmentDataCleaned, ModuleAssessment, session)
    load_csv_to_database(df_averagePGTAHours, AveragePGTAHours, session)
    load_csv_to_database(df_combined_variables, CombinedVariables, session)
    session.close()
    print("Database initialized successfully")

def delete_db():
    Base.metadata.drop_all(engine)
    print("Database deleted successfully")

if __name__ == '__main__':
    init_db()
    # delete_db()
