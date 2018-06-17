from typing import Any, Optional

from django.http import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from services.cache import get_cache
from services.geo import Address
from services.geo.osm import get_address
from .serializers import AddressSerializer

__all__ = (
    'AddressDetailView',
)

cache = get_cache('django')


class AddressDetailView(APIView):
    # noinspection PyMethodMayBeStatic
    def serialize_address(self, address: Address) -> dict:
        """
        Serialize input data to dictionary with the correct key/value pairs

        Given the provided address object, make a dictionary representing the
        address.

        :param address: Input data
        :return: A dictionary representing an Address object
        """
        serializer = AddressSerializer(address)
        return serializer.data

    def _cache_key(self, lon, lat) -> Optional[dict]:
        prefix = getattr(self, 'cache_key_prefix', '')

        # TechDebt: Probably hash this at some point
        return prefix + str(lon) + '--' + str(lat)

    def fetch_address(self, lon: Any, lat: Any) -> Optional[dict]:
        """
        Fetch the address from the remote API and format it as a dict

        The dictionary returned should contain information as specified by
        this API's documentation. This is delegated to `serialize_address`.
        If no valid object can be obtained, we should return None

        :param lon: Location longtitude
        :param lat: Location latitude
        :return: None if any upstream error occurs. Formatted address otherwise.
        """
        address = get_address(lon=lon, lat=lat)
        return self.serialize_address(address)

    def get_address(self) -> dict:
        """
        The equivalent of get_object()

        :return: An Address object serialized to dictionary
        """
        lon = self.request.GET.get('lon', None)
        lat = self.request.GET.get('lat', None)
        if lon is not None and lat is not None:
            key = self._cache_key(lon, lat)
            data = cache.fetch(key)
            if data is None:
                data = self.fetch_address(lon, lat)
                cache.store(key, data)

            return data
        return None

    # noinspection PyShadowingBuiltins
    def get(self, request, format=None):
        obj = self.get_address()
        if obj is None:
            return HttpResponseNotFound()
        return Response(obj)
