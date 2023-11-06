#!/usr/bin/env python3
""" Update topics of school documents based on the name """


def update_topics(mongo_collection, name, topics):
    """ Function that changes all topics of school documents
        based on the name
    """

    result = mongo_collection.update_many(
            {"name": name}, {"$set": {"topics": topics}})
    return result
