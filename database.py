from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a sqlite engine instance
engine = create_engine("sqlite:///employee.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))

# Create the database
Base.metadata.create_all(engine)
