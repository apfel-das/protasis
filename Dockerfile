FROM python:3.9


COPY . /app
COPY ./requirements.txt /app

WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "api:app", "--host=0.0.0.0", "--port=8080", "--reload"]