print('hi this is all about first api in details ')


# fast api code 
from fastapi import FastAPI
app = FastAPI()

@app.get("/")

def hello():
    return 'Hello world'