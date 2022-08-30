from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from confluent_kafka import Producer

app = FastAPI()

producer = Producer({'bootstrap.servers': 'kafka-svc:9092'})


class Note(BaseModel):
    note: str


client = MongoClient(host="database-clusterip-srv",
                     port=27017
                     )

db = client["note"]
collection = db["note_collections"]


def today():
    return str(datetime.today().strftime('%Y-%m-%d'))


@app.post("/note/create")
def new_note(note: Note, date: Optional[str] = today()):
    collection.insert_one({
        "date": date,
        "note": note.note
    })
    producer.produce("notes", value=f"{date},{note.note}")
    return note
