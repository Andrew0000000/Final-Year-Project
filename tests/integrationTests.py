import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from src.database.models import CombinedVariables
from sqlalchemy import create_engine, inspect
from src.database.models import Base
from src.database.databaseLayout import insertModule, deleteModule

DATABASE_URI = 'sqlite:///app_database.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData()
meta.reflect(bind=engine)
table_names = list(meta.tables.keys())
inspector = inspect(engine)
table_names = inspector.get_table_names()

def test_insert_job_description():
    module_code = 'COMP001'
    module_name = 'Introduction to Computer Science'
    number_of_students = 12
    pgtas_recruited = 12
    exam_weight = 10
    coursework_weight = 90
    delivery_code = 'A4U'
    duties = ['teaching', 'marking']
    insertModule(1, module_code, module_name, number_of_students, pgtas_recruited, exam_weight, coursework_weight, delivery_code, duties)
    inserted_module = session.query(CombinedVariables).filter_by(module_code='COMP001').first()
    assert inserted_module is not None
    assert inserted_module.module_code == module_code
    assert inserted_module.module_name == module_name
    assert inserted_module.number_of_students == number_of_students
    assert inserted_module.pgtas_recruited == pgtas_recruited
    assert inserted_module.exam_weight == exam_weight
    assert inserted_module.coursework_weight == coursework_weight
    assert inserted_module.delivery_code == delivery_code
    assert inserted_module.duties == ', '.join(duties)

if __name__ == '__main__':
    test_insert_job_description()
    print("All tests passed!")