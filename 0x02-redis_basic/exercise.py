#!/usr/bin/env python3
""" A module that defines the class Cache """
import redis
from typing import Union, Optional, Callable
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

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, int, float, None]:
        """ Method that retrieves data from Redis. The callable will
            be used to convert the data back to the desired format
        """

        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """ Method that will automatically parametrize Cache.get
            with the correct conversion function str()
        """

        val = self.get(key)

        if val is not None:
            return str(val)
        else:
            return None

    def get_int(self, key: str) -> Union[int, None]:
        """ Method that will automatically parametrize Cache.get
            with the correct conversion function int()
        """

        value = self.get(key)

        if value is not None:
            return int(value)
        else:
            return None
