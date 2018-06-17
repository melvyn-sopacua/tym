from typing import Any, Optional

import requests
from django.conf import settings
from django.http import HttpResponseNotFound
from django.utils.module_loading import import_string
from django.core.exceptions import ValidationError
from services.cache import get_cache
from rest_framework.response import Response
from rest_framework.views import APIView
from urlobject import URLObject
from .serializers import AddressAdapter, AddressSerializer, OSMAdapter

__all__ = (
    'AddressDetailView',
    'OSMAddressView',
)

cache = get_cache('django')


class AddressDetailView(APIView):
    # noinspection PyMethodMayBeStatic
    def get_remote_endpoint(self) -> URLObject:
        """
        Get the remote endpoint

        :return: URLObject for the reverse geocoding endpoint
        """
        base_url = settings.LL2ADDR.get('API_BASE_URL')
        endpoint = settings.LL2ADDR.get('API_ENDPOINT')
        return URLObject(base_url).add_path(endpoint)

    def get_adapter(self) -> AddressAdapter:
        """
        Get the adapter that adapts remote output to serializer input

        Views extending this view can set a property `address_adapter`,
        which is assumed to be an instance of a class extending AddressAdapter.

        If none is provided, the adapter is fetched from settings.

        :return: An instance of a subclass of AddressAdapter
        """
        if not hasattr(self, 'address_adapter'):
            dotted = settings.LL2ADDR.get('ADDRESS_ADAPTER')
            klass = import_string(dotted)
            setattr(self, 'address_adapter', klass())

        return getattr(self, 'address_adapter')

    def serialize_address(self, data: Any) -> dict:
        """
        Serialize input data to dictionary with the correct key/value pairs

        Given the provided data, make dictionary representing the address.

        :param data: Input data
        :return: A dictionary representing an Address object
        """
        adapter = self.get_adapter()
        serializer = AddressSerializer(adapter.get_address(data))
        return serializer.data

    # noinspection PyMethodMayBeStatic
    def clean(self, response):
        """
        Validate if response is correct, then clean and return the data

        Some API's (including OSM) return an error object in JSON, but with a
        200 OK response. This is the hook that should reject input that
        doesn't conform to our standards.

        The default implementation just verifies response.ok and returns the
        the json data converted to native python dict, without modification.

        :param response: requests.Response object
        :return: The JSON data as dict
        """
        if not response.ok:
            raise ValidationError('Response is not OK')
        return response.json()

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
        params = settings.LL2ADDR.get('API_ADDITIONAL_PARAMS', {})
        params['lon'] = lon
        params['lat'] = lat
        url = self.get_remote_endpoint()
        r = requests.get(url, params=params)
        try:
            data = self.clean(r)
        except ValidationError:
            return None
        return self.serialize_address(data)

    def get_address(self) -> dict:
        """
        The equivalent of get_object()

        :return: An Address object serialized to dictionary
        """
        lon = self.request.GET.get('lon', None)
        lat = self.request.GET.get('lat', None)
        if all([lon, lat]):
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


class OSMAddressView(AddressDetailView):
    address_adapter = OSMAdapter()
    valid_address_types = (
        'building',
        'place'
    )
    cache_key_prefix = 'osm--'

    def clean(self, response):
        """
        OSM specific cleaning

        - Only allow 2 address types that are known to give us good data
        - Handle coordinates that cannot be geocoded.

        :param response: requests.Response object
        :return: The JSON data as dict
        """
        data = super().clean(response)
        if 'error' in data:
            raise ValidationError('Unable to geocode coordinates')

        if data.get('addresstype', '') not in self.valid_address_types:
            raise ValidationError('Not a building address')

        return data

