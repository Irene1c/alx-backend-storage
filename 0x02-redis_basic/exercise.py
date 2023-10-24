#!/usr/bin/env python3
""" A module that defines the class Cache """
import redis
from typing import Union, Optional, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Implements a system to count how many times methods
        of the Cache class are called
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Function that increments the count every time the `method`
            is called and returns value returned by the original method
        """

        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Stores history of inputs and outputs for a particular function """

    key1 = method.__qualname__ + ":inputs"
    key2 = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, args):
        """ Function that appends the input arguments """

        self._redis.rpush(key1, f"('{args}',)")

        output = method(self, args)

        self._redis.rpush(key2, output)

        return output

    return wrapper


class Cache:
    """ A class Cache """

    def __init__(self):
        """ class constructor """

        self._redis = redis.Redis()
        self._redis.flushdb()
        self.count_calls = {}

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ A method that generates a random key, stores the input
            data in Redis using the random key and returns the key
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @count_calls
    @call_history
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

    @count_calls
    @call_history
    def get_str(self, key: str) -> Union[str, None]:
        """ Method that will automatically parametrize Cache.get
            with the correct conversion function str()
        """

        val = self.get(key)

        if val is not None:
            return str(val)
        else:
            return None

    @count_calls
    @call_history
    def get_int(self, key: str) -> Union[int, None]:
        """ Method that will automatically parametrize Cache.get
            with the correct conversion function int()
        """

        value = self.get(key)

        if value is not None:
            return int(value)
        else:
            return None
