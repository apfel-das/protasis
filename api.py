from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model import *

app = FastAPI()

@app.get("/status")
def get_status():
    return JSONResponse({
        "name": 'Protasis API v1.0',
        "author": 'apfel-das (Konstantinos Pantelis)'
        })

@app.get("/ratings")
def get_ratings():
    ratings = read_ratings_from_file().head()
    return JSONResponse(ratings.to_dict())

