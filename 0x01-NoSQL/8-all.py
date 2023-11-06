#!/usr/bin/env python3
"""  List all documents in a collection """


def list_all(mongo_collection):
    """ Function that lists all documents in a collection """

    return mongo_collection.find()
