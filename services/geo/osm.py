from getrest.api import Api, RestEndpoint
from getrest.authentication import NoAuthenticationRestAuthenticator
from .adapters import AddressAdapter
from . import Address

__all__ = (
    'NOT_FOUND',
    'OSMAddressAdapter',
    'OSMApi',
    'ReverseGeoEndpoint',
    'get_address'
)

NOT_FOUND = 'No location found'


class OSMAddressAdapter(AddressAdapter):
    field_map = {
        'display': 'display_name',
        'house_nr': 'address.house_number',
        'street': 'address.road',
        'city': 'address.city',
        'province': 'address.state',
        'country': 'address.country',
        'postal_code': 'address.postcode',
        'address_type': 'addresstype',
    }


class ReverseGeoEndpoint(RestEndpoint):
    path = 'reverse_geo'
    actions = ['geo_coords']

    def prepare_request_context(self):
        context = super().prepare_request_context()
        context['params'].update(
            format='jsonv2', addressdetails='1', zoom='18'
        )
        return context


class OSMApi(Api):
    base_url = 'https://nominatim.openstreetmap.org/'
    authenticator = NoAuthenticationRestAuthenticator()
    endpoints = {
        'reverse_geo': (ReverseGeoEndpoint, None)
    }


def get_address(lon, lat):
    api = OSMApi()
    endpoint = api.reverse_geo  # type: ReverseGeoEndpoint
    r = endpoint.geo_coords(lon=lon, lat=lat)
    if r.ok:
        data = r.json()
        if 'error' not in data:
            return OSMAddressAdapter().get_address(data)

    return Address(display=NOT_FOUND)
