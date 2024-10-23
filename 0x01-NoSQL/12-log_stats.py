#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    """
    script that provides some stats about Nginx logs stored in MongoDB
    """

    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx

    n_logs = nginx_logs.count_documents({})
    print(f'{n_logs} logs')
    methods = ["GET", "POST", "PATCH", "PUT", "DELETE"]
    print('Methods:')
    for method in methods
    doc_count = nginx_logs.count_documents({"method": method})
    print(f'\tmethod {method}: {doc_count}')

    check_status = nginx_logs.count_documents(
            {"method": "GET", "path": "/status"}
    )
    print(f'{check_status} check status')
