from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from model import *

app = FastAPI()

api_desciption = """
## **ProtasisApp API** helps you do awesome stuff. 🚀

#### Author

* **apfel-das (Konstantinos T. Pantelis)**
* **GitHub:** 🔗`https://github.com/apfel-das` 
* **LinkedIn:** 🔗`https://www.linkedin.com/in/konstantinos-pantelis-0250201a4/`



### Movies

You can **get movies** from the 100k movie-dataset.

### Users, Ratings

You will be able to:

* **Get users** .
* **Get user ratings** on movies.

### Recommendations

You will be able to:

* **Get recommendations** for movies based on user existent ratings.

## Algorithms used

* **KNN** a.k.a **K-Nearest-Neighbors**.
* **SVD** a.k.a **Singular-Value-Decomposition**.

### Notes

* Only accepting ``GET`` requests for now.
* Can be used as a **standalone API** or along with its ***ReactApp***.


"""

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ProtasisAPI",
        version="1.0.0",
        description=  api_desciption,
        routes=app.routes,
        license_info={
        "name": "License: MIT",
        "url": "https://opensource.org/licenses/MIT",
        },
        contact={
        "name": "GitHub repo.",
        "url": "https://github.com/apfel-das/protasis",
        }
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://i.imgur.com/gY0bg98.png",
        "backgroundColor": "#f5f5f5",
        "altText": 'ProtasisAPI logo'
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Starting")
movies = read_movies_from_file()
ratings = read_ratings_from_file()
users = read_users_from_file()
print("Done")

"""
    Prepopulate predictions.
"""



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
    k = predict_items(ratings, 'knn')
    
    try:
        uid = int(user_id)
        #return JSONResponse(predict_top_for_user(uid, k, 10))

    except:
        return JSONResponse(None)

@app.get("/recommendations/svd/{user_id}")
def get_recommendations_svd(user_id: str):
    s = predict_items(ratings, 'svd')
    try:
        uid = int(user_id)
        #return JSONResponse(predict_top_for_user(uid, s, 10))

    except:
        return JSONResponse(None)
        

