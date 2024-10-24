#!/usr/bin/env python3
"""
Writing and reading a string from Redis and recovering original type,
Incrementing values, Storing lists, Retrieving lists
"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional, Any


def call_history(method: Callable) -> Callable:
    """
    Counts the nr of times the function has been called
    args: function to be wrapped and decorated
    Returns:
       decorated func
    """

    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapped function for the decorated func
        Args: arguments passed to the func
        kwargs: the keyword arg passed to the func
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    counts  how many times methods of the Cache class are called
    args: Function to be decorated
    Return: Decorated function
    """

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Wrapper used for the decorated function

        *Args: is the arguments passed to the function
        **kwargs: Keyword arguments passed to the func

       Return: return value of the decorated func
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Defines method to handle redis cache operations
    """
    def __init__(self):
        """
        Initializes redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in redis cache
        Args: data (dict): data to be stored
        Returns: str: key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Gets data from the redis cache
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Gets the data as string from redis cache
        args: key
        Return: Data
        """
        data = self.get(key, lambda x: x.decod('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Gets the data as int from redic cache
        Args:key

        Return: Int
        """
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data


def replay(method: Callable):
    """
    Rplays history of a func
    Args: func to be decorated

    Returns: None
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(inputList, outputList))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
