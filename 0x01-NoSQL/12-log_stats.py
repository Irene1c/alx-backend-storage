#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # number of documents the collection
    x = collection.count_documents({})
    print(f"{x} logs")

    #  number of documents with the method =
    # ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print("Methods:")

    for m in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        num = collection.count_documents({"method": m})
        print(f"\tmethod {m}: {num}")

    # number of documents with method=GET and path=/status
    count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{count} status check")
