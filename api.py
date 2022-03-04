from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model import *
import json

app = FastAPI()


movies = read_movies_from_file()
ratings = read_ratings_from_file()
users = read_users_from_file()

"""
    Prepopulate predictions.
"""
k = predict_items(ratings, 'knn')
s = predict_items(ratings, 'svd')


@app.get("/status")
def get_status():
    return JSONResponse({
        "name": 'Protasis API v1.0',
        "author": 'apfel-das (Konstantinos Pantelis)'
        })
 
@app.get("/ratings")
def get_ratings():
    result = []

    """
        Adjust the ratings DataFrame.
    """
    
    for row in ratings.iterrows():
        
        r = {
            "user_id" : str(row[1]['user_id']),
            "movie_id": str(row[1]['movie_id']),
            "rating": str(row[1]['rating'])
        }
        
        result.append(r)
    
    return JSONResponse(result)

@app.get("/movies")
def get_movies():
    
    result = []
    for row in movies.iterrows():
        r = {
            "movie_id" : str(row[1]['movie_id']),
            "title": str(row[1]['title']),
            "imdb_url": str(row[1]['IMDb URL'])
        }
        result.append(r)

    return JSONResponse(result)

@app.get("/users")
def get_users():
    
    result = []
    for row in users.iterrows():
        r = {
            "user_id" : str(row[1]['user_id']),
            "age": str(row[1]['age']),
            "sex": str(row[1]['sex']),
            "occupation": str(row[1]['occupation'])
        }
        result.append(r)

    return JSONResponse(result)


@app.get("/recommendations/knn/{user_id}")
def get_recommendations_knn(user_id: str):
    
    try:
        uid = int(user_id)
        return JSONResponse(predict_top_for_user(uid, k, 10))

    except:
        return JSONResponse(None)

@app.get("/recommendations/svd/{user_id}")
def get_recommendations_svd(user_id: str):
    
    try:
        uid = int(user_id)
        return JSONResponse(predict_top_for_user(uid, s, 10))

    except:
        return JSONResponse(None)
        

