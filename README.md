# protasis
A movie recommendation engine (which doesn't yet exist) made under FastAPI (yup, I like experimenting).


## How to run:
- Clone the repository
- Create a `.env` file and add following lines:
  ```
    RATINGS_FILE='u.data'
    MOVIES_FILE='u.item'
    USERS_FILE='u.user'
    
  ```
 - Install dependencies (`pip install requirements.txt` will do).
 - Deploy on a local server (`uvicorn api:app --host localhost --port <some_port> --reload` will do).
 - Navigate to `localhost:8080/docs` and read the docs.
