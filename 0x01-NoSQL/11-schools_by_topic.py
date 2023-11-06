#!/usr/bin/env python3
"""  List of schools having a specific topic """


def schools_by_topic(mongo_collection, topic):
    """ Function that returns list of schools having a specific topic"""

    return mongo_collection.find({"topics": topic})
