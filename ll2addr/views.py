from typing import Any, Optional

import requests
from django.conf import settings
from django.http import Http404
from django.utils.module_loading import import_string
from rest_framework.response import Response
from rest_framework.views import APIView
from urlobject import URLObject
from .serializers import AddressAdapter, AddressSerializer


class AddressDetail(APIView):
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
        :return:
        :rtype:
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
        if not r.ok:
            return None
        return self.serialize_address(r.json())

    def get_address(self) -> dict:
        """
        The equivalent of get_object()

        :return: An Address object serialized to dictionary
        """
        lon = self.request.GET.get('lon', None)
        lat = self.request.GET.get('lat', None)
        if all([lon, lat]):
            return self.fetch_address(lon, lat)
        return None

    # noinspection PyShadowingBuiltins
    def get(self, request, format=None):
        obj = self.get_address()
        if obj is None:
            return Http404
        return Response(obj)
