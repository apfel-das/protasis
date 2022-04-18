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
    assert response.status_code == 200, "Response returned NOT OK!"
    assert len(response.json()) == user_count, "Response has different element count than expected!"
    assert list(response.json()[0].keys()) == user_object_keys, "Response has different keys than expected!"
    
"""
    Tests that /movies enpoint is up and working properly.
"""
def test_get_movies():
    movie_count = 1682
    movie_object_keys = ['movie_id', 'title', 'imdb_url']

    response = client.get("/movies")
    assert response.status_code == 200, "Response returned NOT OK!"
    assert len(response.json()) == movie_count, "Response has different element count than expected!"
    assert list(response.json()[0].keys()) == movie_object_keys, "Response has different keys than expected!"



"""
    Tests that /ratings enpoint is up and working properly.
"""
def test_get_ratings():
    rating_count = 100000
    rating_object_keys = ['user_id', 'movie_id', 'rating']

    response = client.get("/ratings")
    assert response.status_code == 200, "Response returned NOT OK!"
    assert len(response.json()) == rating_count, "Response has different element count than expected!"
    assert list(response.json()[0].keys()) == rating_object_keys, "Response has different keys than expected!"


"""
    Tests that /recommendations/knn/some_id enpoint is up and working properly.
"""
def test_knn_recommendation_endpoints_return_proper():
    some_id = 571
    response = client.get("/recommendations/knn/"+str(some_id))

    assert response.status_code == 200, "Response returned NOT OK!"
    assert type(response.json()) == list, "Response is not a list!"
    assert len(response.json()) == 10, "Response has more elements than expected!"

"""
    Tests that /recommendations/svd/some_id enpoint is up and working properly.
"""
def test_svd_recommendation_endpoints_return_proper():
    some_id = 571
    response = client.get("/recommendations/svd/"+str(some_id))

    assert response.status_code == 200, "Response returned NOT OK!"
    assert type(response.json()) == list, "Response is not a list!"
    assert len(response.json()) == 10, "Response has more elements than expected!"

"""
    Tests all valid endpoints for allowing POST requests.
"""
def test_post_request_not_allowed():
    endpoints = ['/status', '/users', '/ratings', '/movies', '/recommendations/knn/571', '/recommendations/svd/571']

    for endpoint in endpoints:
        response = client.post(
            endpoint,
            json={"id": "foobar", "title": "Foo Bar", "description": "Just messing up"},
        )    
        # POST request not allowed --> 405.
        assert response.status_code == 405, "Response returned wrong! (It should return NOT ALLOWED [405])!"


