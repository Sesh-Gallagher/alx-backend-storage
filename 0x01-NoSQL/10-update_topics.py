#!/usr/bin/env python3
"""
Python function that changes all topics
of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    """
    search = {"name": name}
    new_value = {"$set": {"topics": topics}}

    mongo_collection.update_many(search, new_value)
