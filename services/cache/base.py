"""
A Cache Service
---------------

A cache has 2 core api's:
- fetch
- store

In addition, managing the cache deals with 2 more api's:
- remove
- clear

Everything else are derivatives of the above or implementation details.

This cache abstraction assumes that expiring old entries is a task of the
backend and not part of the public API. There is no support for transactions
or locking mechanisms.
"""
from typing import Optional, Any


class CacheBase(object):
    CACHE_FOREVER = -1
    DONT_CACHE = 0
    EXP_DFLT = 300

    def __init__(self, **kwargs):
        """
        Initialize cache

        Any configuration parameters needed should be passed through keyword
        arguments.
        """
        pass

    def fetch(self, key: str) -> Optional[Any]:
        """
        Get a cache entry by key

        :param key: The cache key
        :return: The data if available or `None` otherwise.
        """
        raise NotImplementedError('Cache implementations shall implement '
                                  'fetch()')

    def store(self,
              key: str, data: Any,
              expires: Optional[int] = EXP_DFLT) -> bool:
        """
        Store data into the cache with given expiration time

        The implementation should handle exceptions that are common for the
        backend or implementation and return `false` if storing the data fails.
        Any exceptions that cannot be reasonably foreseen should remain
        uncaught.
        If the timeout resolves to `self.DONT_CACHE` this is allowed to be a
        no-op and return True regardless, since the request was completed
        successfully.

        :param key: Key to identify the data with
        :param data: data to store
        :param expires: seconds till the entry expires
        :return: whether the data was stored
        """
        raise NotImplementedError('Cache implementations shall implement '
                                  'store()')

    def store_forever(self, key: str, data: Any) -> bool:
        """
        Shortcut to store data in the cache forever

        This stores the data without expiration or far enough in the future
        that the expiration time is practially "never".
        This shortcut is available allowing different implementations to come up
        with their own "expriationless" storage mechanism. This should be
        reflected in the `CACHE_FOREVER` class property.

        :param key: Key to identify the data with
        :param data: data to store
        :return: whether the data was stored.
        """
        return self.store(key, data, expires=self.CACHE_FOREVER)

    def remove(self, key: str) -> None:
        """
        Remove an entry

        Removes an entry identified by the key. If the entry does not exist,
        this method will fail silently.

        :param key: key for the cache entry
        :return: None
        """
        raise NotImplementedError('Cache implementations shall implement '
                                  'remove()')

    def clear(self) -> None:
        """
        Remove all items from the cache.

        :return: None
        """
        raise NotImplementedError('Cache implentations shall define a clear '
                                  'method')
