from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from confluent_kafka import Producer

app = FastAPI()

producer = Producer({'bootstrap.servers': 'localhost:9092'})


class ToDo(BaseModel):
    to_do: str


client = MongoClient(host="0.0.0.0",
                     port=27017,
                     username="admin",
                     password="admin"
                     )

db = client["reminder"]
collection = db["reminder_collections"]


def today():
    return datetime.today().strftime('%Y-%m-%d')


@app.post("/")
def new_reminder(reminder: ToDo, date: Optional[str] = today()):
    if not collection.find_one():
        collection.insert_one({
            "date": date,
            "to_do": reminder.to_do,
        })
        producer.produce("reminders", value=f"{date},{reminder.to_do}")
        return reminder
    else:
        return "To do list for today has already been created"


@app.get("/")
def root():
    if collection.find_one():
        return str(collection.find_one())
    else:
        return "No reminders, wanna create one?"
    # return {"message": "Reminder API"}


@app.get("/hello")
def sayhello():
    return "Hello World"
