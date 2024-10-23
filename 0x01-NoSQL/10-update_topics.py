#!/usr/bin/env python3
"""
Python function that changes all topics
of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    """

    return mongo_colletion.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
