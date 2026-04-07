from fastapi import FastAPI, Path #import FastAPI like an object
from typing import Optional
from pydantic import BaseModel

app = FastAPI() 

#amazon.com/create-user(post some data to that endpoint to create user)
#Create an endpoint (one end of communication channel)

# GET - GET AN INFORMATION
# POST - CREATE SOMETHING NEW
# PUT - UPDATE
# DELETE - DELETE SOMETHING

#Create new API
# app is FastAPI Application
# .get(...) means enpoint respons to a GET request
# "/" means the root URL
# @ means this function is runnning on URL (and will run when someone interacts)

# An endpoint is a specific URL where your API can be accessed to perform an action 
students = {
    1: {
        "name": "john",
        "age": 17, 
        "year": "Year 12"
    }  
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/") # It tells if someone goes to the homepage of my API, run the function below
def index():
    return {"name": "First Data"} #JSON Data

@app.get("/get-student/{student_id}") #student_id should be collected
# :int -> student_id must be an integer
# Path(...) -> this value comes from the URL path
# ... -> This value is required #gt -> greater than # lt -> less than
def get_student(student_id: int = Path(..., 
                description="The ID of the student you want to view", 
                gt=0, lt=10)): 
    return students[student_id]  

@app.get("/get-by-name")
# google.com/results?search=Python -> URL
def get_student(*, student_id: int, name: str| None = None, test: int):
    for s_id in students:
        if students[s_id]["name"] == name and s_id == student_id:
            return students[student_id]
    return {"Data": "Not found"}

# Create new student Object
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if student_id in students:
        return {"Error": "Student exists"}
    
    students[student_id] = student
    return students[student_id]

#Put Method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"} # Find the ID
    
    if student.name != None:
        students[student_id].name = student.name 
        # students[student_id].name = current value in data base
        # student.name new value just typed into the API
        # Check your name input from server. 
        # Since you didn't send a name, it is None. The code skips this.
    
    if student.age != None:
        students[student_id].age = student.age
        #You sent 15. This is not None.
        #The code runs: students[1]["age"] = 15. The old 12 is overwritten by 15.
    
    if student.year != None:
        students[student_id].year = student.year
        # This is None. The code skips this. 
        # The original year (e.g., "Year 12") is safe.

    return students[student_id]

@app.delete("/delete-student/{student-id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": " Student deleted successfully"}