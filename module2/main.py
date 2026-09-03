from fastapi import FastAPI
import json

app=FastAPI()
# load data from json file when we need the student data read
def load_data():
    with open('students.json','r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return "Students management system API"

@app.get('/about')
def about():
    return "A fully functional api to manage our students records"

# we read the json file data http method using get method
@app.get('/view')
def view_students():
    data = load_data()
    return data
    