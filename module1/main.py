print('hi this is all about first api in details ')


# fast api code 
from fastapi import FastAPI
app = FastAPI()

@app.get("/")# simple get request 

def hello():
    return 'Hello world'

@app.get("/about")# simple get request 

def about():
    return 'Hello world from about page'