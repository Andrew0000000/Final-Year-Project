from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT

Base = declarative_base()

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    course_code = Column(String(50))
    term = Column(String(50))
    total_hours = Column(Integer)
    lecture_hours = Column(Integer)
    tutorial_hours = Column(Integer)
    lab_hours = Column(Integer)
    duties = Column(String(255))
    topics = Column(String(255))
    description = Column(LONGTEXT)  # LONGTEXT for longer text fields in MySQL

 