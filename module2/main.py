from fastapi import FastAPI, Path, HTTPException, Query, Body
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated


app = FastAPI()

# apply pydantic to data validation
class student(BaseModel):
    id:Annotated[str,Field(...,description="student id of the student",example='s001')]
    name: str
    age:Annotated[int,Field(...,gt=0,lt=100,description="student age",example='12')]
    student_class:Annotated[int,Field(...,description="student id of the student",example='s001')]
    roll: Annotated[int,Field(...,gt=0,lt=100)]
    math_marks:Annotated[int,Field(...,gt=0,lt=101)]
    english_marks:Annotated[int,Field(...,gt=0,lt=101)]
    science_marks:Annotated[int,Field(...,gt=0,lt=100)]
    phone_number: Annotated[str,Field(...,example='01724397441')]


def load_data():
    with open("students.json", "r") as f:
        data = json.load(f)

    return data


def save_data(data):
    with open("students.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return "Student Management System API"


@app.get("/about")
def about():
    return "A fully functional API to manage our student records"


@app.get("/view")
def view_students():
    data = load_data()

    return data


@app.get("/view/{student_id}")
def view_student_by_id(
    student_id: str = Path(
        ...,
        description="Student id of the student",
        example="S001"
    )
):
    data = load_data()

    if student_id in data:
        return data[student_id]

    else:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )


@app.get("/sort")
def view_sorted_students(
    sorted_by: str = Query(
        ...,
        description="Sort on the basis of class, age, roll, marks"
    ),
    order: str = Query(
        "asc",
        description="choose order: asc or desc"
    )
):
    valid_fields = [
        "age",
        "student_class",
        "roll",
        "Math marks",
        "English marks",
        "Science marks",
    ]

    if sorted_by not in valid_fields:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid field, select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=404,
            detail="Choose between asc or desc"
        )

    data = load_data()

    if order == "asc":
        sorted_data = list(data.values())

        sorted_data.sort(
            key=lambda x: x[sorted_by]
        )

        return sorted_data

    else:
        sorted_data = list(data.values())

        sorted_data.sort(
            key=lambda x: x[sorted_by],
            reverse=True
        )

        return sorted_data

# create post method in database 

@app.post("/create")
def create_student(student: student):
    data = load_data()

    student_id = student.id

    # same id jeno  handle kore input neoyar somoy

    if student.id in data:
        raise HTTPException(status_code=400,detail='student id already exits')

    data[student_id] = student.model_dump(exclude=['id'])

    save_data(data)


    return  JSONResponse(status_code=201,content="Successfully student created")

# use pydantic to data validation  in details to check all the validation

# now update the data using put request


