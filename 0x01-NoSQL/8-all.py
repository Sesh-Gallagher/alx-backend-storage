#!usr/bin/env python3
"""
Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    List of all documents in python
    """

    allDocuments = mongo_collection.find()

    if allDocuments.count() == 0:
        return []

    return allDocuments
