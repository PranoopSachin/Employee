import uvicorn

from fastapi import FastAPI, status

from database import Base, Employee, engine

from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode


# Create employee request Base Model
class EmployeeRequest(BaseModel):
    id : int
    name: str
# Create the database
Base.metadata.create_all(engine)

app = FastAPI()


@app.post("/create-employee", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeRequest):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the Employee database model
    employeedb = Employee(name = employee.name)

    # add it to the session and commit it
    session.add(employeedb)
    session.commit()

    # grab the id given to the object from the database
    id = employee.id

    # close the session
    session.close()

    # return the id
    return f"created employee with id {id}"

@app.get("/employee/{id}")
async def get_employee(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the employee name with the given id
    employee = session.query(Employee).get(id)

    # close the session
    session.close()

    return f"employee  with id: {employee.id} and name: {employee.name}"
    

@app.get("/employee-list")
def read_employee_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all employees
    employee_list = session.query(Employee).all()

    # close the session
    session.close()

    return employee_list


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
