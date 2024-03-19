import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database.models import CombinedVariables
from src.database.models import Base
from src.ml_models.modelLoading import load_model
from src.prediction_prompts.linearRegPrompt import linearRegressionPredictor
from src.prediction_prompts.ridgeRegPrompt import ridgeRegressionPredictor
from src.prediction_prompts.gamPrompt import gamPredictor
from src.prediction_prompts.featureEngPrompt import featureEngineeringPredictor
from src.prediction_prompts.vectoriserPrompt import vectoriserPredictor


# ===============================
# TESTING FOR DATABASE OPERATIONS
# ===============================

# Adjust the DATABASE_URI to use an in-memory SQLite database
DATABASE_URI = 'sqlite:///:memory:'

@pytest.fixture(scope="function")
def session():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_insert_module(session):
    module_code = 'COMP001'
    module_name = 'Introduction to Computer Science'
    number_of_students = 12
    pgtas_recruited = 12
    exam_weight = 10
    coursework_weight = 90
    delivery_code = 'A4U'
    duties = ['teaching', 'marking']
    new_module = CombinedVariables(
        module_code=module_code,
        module_name=module_name,
        number_of_students=number_of_students,
        pgtas_recruited=pgtas_recruited,
        exam_weight=exam_weight,
        coursework_weight=coursework_weight,
        exam_coursework_ratio=f'{exam_weight}:{coursework_weight}',
        delivery_code=delivery_code,
        duties=(', ').join(duties),
    )
    session.add(new_module)
    session.commit()
    inserted_module = session.query(CombinedVariables).filter_by(module_code='COMP001').first()
    assert inserted_module is not None

def test_delete_module(session):
    module_code = 'COMP001'
    module_name = 'Introduction to Computer Science'
    number_of_students = 12
    pgtas_recruited = 12
    exam_weight = 10
    coursework_weight = 90
    delivery_code = 'A4U'
    duties = ['teaching', 'marking']
    new_module = CombinedVariables(
        module_code=module_code,
        module_name=module_name,
        number_of_students=number_of_students,
        pgtas_recruited=pgtas_recruited,
        exam_weight=exam_weight,
        coursework_weight=coursework_weight,
        exam_coursework_ratio=f'{exam_weight}:{coursework_weight}',
        delivery_code=delivery_code,
        duties=(', ').join(duties),
    )
    session.add(new_module)
    session.commit()
    module = session.query(CombinedVariables).filter(CombinedVariables.module_code == 'COMP001').first()
    assert module is not None
    session.delete(module)
    session.commit()
    module = session.query(CombinedVariables).filter(CombinedVariables.module_code == 'COMP001').first()
    assert module is None

def test_fetch_data(session):
    module_code = 'COMP001'
    module_name = 'Introduction to Computer Science'
    number_of_students = 12
    pgtas_recruited = 12
    exam_weight = 10
    coursework_weight = 90
    delivery_code = 'A4U'
    duties = ['teaching', 'marking']
    new_module = CombinedVariables(
        module_code=module_code,
        module_name=module_name,
        number_of_students=number_of_students,
        pgtas_recruited=pgtas_recruited,
        exam_weight=exam_weight,
        coursework_weight=coursework_weight,
        exam_coursework_ratio=f'{exam_weight}:{coursework_weight}',
        delivery_code=delivery_code,
        duties=(', ').join(duties),
    )
    session.add(new_module)
    session.commit()
    inserted_module = session.query(CombinedVariables).filter_by(module_code='COMP001').first()
    assert inserted_module.module_code == module_code
    assert inserted_module.module_name == module_name
    assert inserted_module.number_of_students == number_of_students
    assert inserted_module.pgtas_recruited == pgtas_recruited
    assert inserted_module.exam_weight == exam_weight
    assert inserted_module.coursework_weight == coursework_weight
    assert inserted_module.delivery_code == delivery_code
    assert inserted_module.duties == ', '.join(duties)


# ===============================================
# TESTING FOR MACHINE LEARNING PREDCITION PROMPTS
# ===============================================


def test_linear_regression_prompt():
    model = load_model('linear_model.pkl')
    assert model is not None
    output = linearRegressionPredictor(1, 120, 10, 90, 'A4U')
    result = float(output.split(' ')[-1])
    assert result > 50
    assert result < 250

def test_ridge_regression_prompt():
    model = load_model('ridge_model.pkl')
    assert model is not None
    output = ridgeRegressionPredictor(1, 120, 10, 90, 'A4U')
    result = float(output.split(' ')[-1])
    assert result > 50
    assert result < 250

def test_gam_prompt():
    model = load_model('gam_model.pkl')
    assert model is not None
    output = gamPredictor(1, 120, 10, 90, 'A4U')
    result = float(output.split(' ')[-1])
    assert result > 50
    assert result < 250

def test_feature_engineering_prompt():
    model = load_model('feature_engineering_model.pkl')
    assert model is not None
    duties = [
        'Supporting scheduled sessions (computing lab / tutorial / class etc )', 
        'Providing student support (e.g. Moodle Q&A, office hours)', 
        'Facilitating student teams (e.g. projects)', 
        'Marking - other (e.g. coursework, coding activities, in class tests, formative assessment, etc)',
    ]
    output = featureEngineeringPredictor(1, duties)
    result = float(output.split(' ')[-1])
    assert result > 50
    assert result < 250

def test_vectoriser_prompt():
    model = load_model('TF-IDF_model.pkl')
    assert model is not None
    duties = [
        'Supporting scheduled sessions (computing lab / tutorial / class etc )', 
        'Providing student support (e.g. Moodle Q&A, office hours)', 
        'Facilitating student teams (e.g. projects)', 
        'Marking - other (e.g. coursework, coding activities, in class tests, formative assessment, etc)',
    ]
    output = vectoriserPredictor(1, duties)
    result = float(output.split(' ')[-1])
    assert result > 50
    assert result < 250
