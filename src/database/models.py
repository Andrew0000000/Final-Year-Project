from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float

Base = declarative_base()

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    module_code = Column(String)
    term = Column(String)
    total_hours_excluding_marking = Column(Integer)
    marking_hours_excluding_exam = Column(Integer)
    marking_hours_exam = Column(Integer)
    TA_needed = Column(Integer)
    duties = Column(String)
    categories = Column(String)
    description = Column(Text)
    total_hours = Column(Integer)

class RequestedVsRecruited(Base):
    __tablename__ = 'requested_vs_recruited'
    id = Column(Integer, primary_key=True)
    module_code = Column(String)
    module_title = Column(String)
    variant = Column(String)
    module_code_and_title = Column(String)
    is_module_new = Column(String)
    requested_23_24 = Column(Integer)
    recruited_23_24 = Column(Integer)
    requested_22_23 = Column(Integer)
    recruited_22_23 = Column(Integer)
    requested_21_22 = Column(Integer)
    recruited_21_22 = Column(Integer)
    notes = Column(Text)

class CapVsActualStudents(Base):
    __tablename__ = 'cap_vs_actual_students'
    id = Column(Integer, primary_key=True)
    module_code = Column(String)
    module_title = Column(String)
    cap_23_24 = Column(Integer)
    actual_22_23 = Column(Integer)
    notes = Column(Text)

class ModuleAssessment(Base):
    __tablename__ = 'module_assessment'
    id = Column(Integer, primary_key=True)
    module_code = Column(String)
    delivery_code = Column(String)
    module_delivery_period_code = Column(String)
    assessment_sequence = Column(Integer)
    assessment_type_code = Column(String)
    assessment_type_name = Column(String)
    assessment_title = Column(String)
    coursework_weight = Column(Float)
    exam_weight = Column(Float)
    exam_coursework_ratio = Column(String)

class CombinedVariables(Base):
    __tablename__ = 'combined_variables'
    id = Column(Integer, primary_key=True)
    module_code = Column(String)
    number_of_students = Column(Integer)
    pgtas_recruited = Column(Integer)
    exam_coursework_ratio = Column(String)
    exam_weight = Column(Integer)
    coursework_weight = Column(Integer)
    delivery_code = Column(String)
    total_hours = Column(Integer)
    duties = Column(String)
    
    

class AveragePGTAHours(Base):
    __tablename__ = 'average_pgta_hours'
    id = Column(Integer, primary_key=True)
    duties = Column(String)
    average_hours = Column(Float)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    department = Column(String)
    faculty = Column(String)






 