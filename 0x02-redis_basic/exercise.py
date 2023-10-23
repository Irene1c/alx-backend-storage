#!/usr/bin/env python3
""" A module that defines the class Cache """
import redis
from typing import Union
import uuid


class Cache:
    """ A class Cache """

    def __init__(self):
        """ class constructor """

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ A method that generates a random key, stores the input
            data in Redis using the random key and returns the key
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
