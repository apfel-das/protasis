# protasis-api
A movie recommendation engine (which doesn't yet exist) made under FastAPI, Surprise and the 100k movies dataset (yup, I like experimenting a lot).


## How to run:
- Clone the repository
 - Install dependencies (`pip3 install -r requirements.txt` will do).
 - Deploy on a local server (`uvicorn api:app --host localhost --port <some_port> --reload` will do).
 - Navigate to `localhost:8080/docs` and read the docs.

## How to Docker-run:
- There is a dockerfile 😂.
- So build it  (`docker build -t protasis-api` will do)
- Deploy from `8080` (like `docker run -pd 8080 protasis-api .`)
- Have fun..
