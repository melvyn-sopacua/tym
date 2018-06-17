from typing import Optional, Any
from .base import CacheBase
from django.core import cache


class DjangoCache(CacheBase):
    CACHE_FOREVER = None
    EXP_DFLT = 30

    def __init__(self, cache_alias: str=cache.DEFAULT_CACHE_ALIAS, **kwargs):
        self._backend = cache.caches[cache_alias]
        super().__init__(**kwargs)

    def fetch(self, key: str) -> Optional[Any]:
        return self._backend.get(key, None)

    def store(self,
              key: str, data: Any, expires: Optional[int]=EXP_DFLT) -> bool:
        if expires == self.DONT_CACHE:
            return True
        try:
            self._backend.set(key, data, expires)
        except RuntimeError:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        return self._backend.delete(key)

    def clear(self):
        self._backend.clear()
