from pymongo import MongoClient
from confluent_kafka import Consumer


client = MongoClient(host="0.0.0.0",
                     port=27017,
                     username="admin",
                     password="admin"
                     )

db = client["query"]
collection = db["query_collections"]

reminder_consumer = Consumer({"bootstrap.servers": "localhost:9092",
                              "group.id": "FastAPI",
                              "enable.auto.commit": True,
                              "auto.offset.reset": "beginning"})
reminder_consumer.subscribe(["reminders"])


note_consumer = Consumer({"bootstrap.servers": "localhost:9092",
                          "group.id": "FastAPI",
                          "enable.auto.commit": False,
                          "auto.offset.reset": "beginning"})
note_consumer.subscribe(["notes"])


def event_stream():
    while True:
        msg = reminder_consumer.poll(timeout=0.5)
        notes = note_consumer.poll(timeout=0.5)
        if msg is not None:
            message = msg.value().decode("utf-8")
            print(message)
            message_seperated = message.split(sep=",")
            collection.insert_one({
                "date": message_seperated[0],
                "to_do": message_seperated[1],
                "note": []
            })
        elif notes is not None:
            notes = notes.value().decode("utf-8")
            print(notes)
            notes_seperated = notes.split(sep=",")
            collection.update_one({"date": "2022-08-26"},
                                  {"$push": {"note": {"$each": [f"{notes_seperated[1]}"]}}})
        elif msg is None:
            pass
        else:
            pass


if __name__ == '__main__':
    event_stream()
