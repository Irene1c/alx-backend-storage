#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
from functools import wraps
import redis
import requests
from typing import Callable


r = redis.Redis()


def count_url(func: Callable) -> Callable:
    """Implementing how many times a particular URL was accessed """

    @wraps(func)
    def wrapper(url: str) -> str:
        """ Tracking how many times a particular URL was accessed in the key
            and cache the result with an expiration time of 10 seconds
        """

        result = func(url)

        key = f"count:{url}"
        if result:
            r.incr(key)
            r.expire(key, 10)

        return result

    return wrapper


@count_url
def get_page(url: str) -> str:
    """ Function that request HTML content of a particular URL """

    response = requests.get(url)
    data = response.text
    return data
