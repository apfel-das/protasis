from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

"""
    Tests that /status endpoint is up.
"""
def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {
        "name": 'Protasis API v1.0',
        "author": 'apfel-das (Konstantinos Pantelis)'
        }

"""
    Tests that /users enpoint is up and working properly.
"""
def test_get_users():
    user_count = 943
    user_object_keys = ['user_id', 'age', 'sex', 'occupation']

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == user_count
    assert list(response.json()[0].keys()) == user_object_keys
    
"""
    Tests that /movies enpoint is up and working properly.
"""
def test_get_movies():
    movie_count = 1682
    movie_object_keys = ['movie_id', 'title', 'imdb_url']

    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == movie_count
    assert list(response.json()[0].keys()) == movie_object_keys



"""
    Tests that /ratings enpoint is up and working properly.
"""
def test_get_ratings():
    rating_count = 100000
    rating_object_keys = ['user_id', 'movie_id', 'rating']

    response = client.get("/ratings")
    assert response.status_code == 200
    assert len(response.json()) == rating_count
    assert list(response.json()[0].keys()) == rating_object_keys