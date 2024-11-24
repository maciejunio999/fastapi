from fastapi import FastAPI, Path
from typing import Optional

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

@app.get("/")
def index():
    return {"name": "First Data"}

# path parameter
@app.get("/get_student/{student_id}")
def get_student(student_id: int = Path(description='The ID of student we wont to view', gt=0, lt=5)):
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

