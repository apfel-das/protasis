from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from model import *
from os.path import exists

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


movies = read_movies_from_file()
ratings = read_ratings_from_file()
users = read_users_from_file()
PREDICTION_FILE_KNN = 'predictions_knn'
PREDICTION_FILE_SVD = 'predictions_svd'


"""
    Prepopulate predictions.
"""

k = []
s = []

def prepoluate_predictions():
    k = predict_items(ratings, 'knn', PREDICTION_FILE_KNN)
    s = predict_items(ratings, 'svd', PREDICTION_FILE_SVD)

@app.get("/init")
async def init_api(background_tasks: BackgroundTasks):
    background_tasks.add_task(prepoluate_predictions)
    return JSONResponse({"status":"Initializing model.."})

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
    
    if(len(k) == 0) and (not exists("./"+PREDICTION_FILE_KNN)):
        return JSONResponse({"error": "Model not yet computed or not initialized."})

    try:
        uid = int(user_id)
        return JSONResponse(predict_top_for_user(uid, "./"+PREDICTION_FILE_KNN, 10))

    except:
        return JSONResponse(None)

@app.get("/recommendations/svd/{user_id}")
def get_recommendations_svd(user_id: str, background_tasks: BackgroundTasks):
    if(len(s) == 0 and (not exists("./"+PREDICTION_FILE_SVD))):
        print(s)
        return JSONResponse({"error": "Model not yet computed or not initialized."})

    try:
        uid = int(user_id)
        return JSONResponse(predict_top_for_user(uid, "./"+PREDICTION_FILE_SVD, 10))

    except:
        return JSONResponse(None)
        

