from fastapi import FastAPI
from pymongo import MongoClient


client = MongoClient(host="0.0.0.0",
                     port=27017,
                     username="admin",
                     password="admin"
                     )

db = client["query"]
collection = db["query_collections"]

app = FastAPI()


@app.get("/")
def root():
    if collection.find_one():
        return str(collection.find_one())
    else:
        return "No reminders, please create one?"
    # return {"message": "Reminder API"}


@app.get("/hello")
def sayhello():
    return "Hello World"
