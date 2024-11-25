from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


students = {
    1: {
        "name": "Maciek",
        "age": 24,
        "hoodie": True
    },
    2: {
        "name": "Julia",
        "age": 23,
        "hoodie": False
    }
}


class Student(BaseModel):
    name: str
    age: int
    hoodie: bool

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    hoodie: Optional[bool] = None


@app.get("/")
def index():
    return {"name": "First Data"}

# path parameter
@app.get("/get_student/{student_id}")
def get_student(student_id: int = Path(description='The ID of student we wont to view', gt=0, lt=5)):
    if student_id not in students:
        return {"Error": "Student does not exist!"}
    return students[student_id]

# query parameter
@app.get("/get_by_name")
def get_student(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
    return {"Data": "Not found"}

# both query and path parameter
@app.get("/get_by_name_and_id/{student_id}")
def get_student(*, name: Optional[str] = None, student_id: int):
    for s_id in students:
        if students[student_id]['name'] == name and s_id == student_id:
            return students[student_id]
    return {"Data": "Not found"}

# post request
@app.post('/create_strudent/{student_id}')
def create_strudent(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Strudent exists"}
    else:
        students[student_id] = student
        return students[student_id]

# put request
@app.put('/update_student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist!"}
    
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.hoodie != None:
        students[student_id].hoodie = student.hoodie

    return students[student_id]

@app.delete('/delete_student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist!"}
    
    del students[student_id]
    return {"Message": "Student deleted"}