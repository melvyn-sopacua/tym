from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
import requests
from urlobject import URLObject
from django.conf import settings
from typing import Any, Optional


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

    def format_address(self, data: dict) -> dict:
        return data

    def fetch_address(self, lon, lat) -> Optional[dict]:
        """
        Fetch the address from the remote API and format it as a dict

        The dictionary returned should contain information as specified by
        this API's documentation. This is delegated to `format_address`.
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
        return self.format_address(r.json())

    def get_address(self):
        lon = self.request.GET.get('lon', None)
        lat = self.request.GET.get('lat', None)
        if all([lon, lat]):
            return self.fetch_address(lon, lat)
        return None

    def get(self, request, format=None):
        obj = self.get_address()
        if obj is None:
            return Http404
        return Response(obj)
