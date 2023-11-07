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

    # top 10 of the most present IPs in the collection (aggregation)
    print("IPs:")
    result = collection.aggregate(
            [
                {"$group": {"_id": "$ip", "ttl": {"$sum": 1}}},
                {"$sort": {"ttl": -1}},
                {"$limit": 10}
                ])

    for i in result:
        print(f"\t{i['_id']}: {i['ttl']}")
