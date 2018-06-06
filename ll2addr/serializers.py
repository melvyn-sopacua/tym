from rest_framework import serializers
import operator
from functools import reduce


__all__ = (
    'AddressSerializer',
    'AddressAdapter',
    'OSMAdapter',
    'Address'
)


# This could be a named tuple in current form.
class Address(object):
    def __init__(self,
                 display='', house_nr='', street='', city='',
                 postal_code='', province='', country='', **kwargs):
        self.display = display
        self.house_nr = house_nr
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.province = province
        self.country = country
        self.address_type = kwargs.get('address_type', 'building')


class AddressAdapter(object):
    field_map = {}

    def __init__(self):
        self.data = None
        if not self.field_map:
            raise ValueError('No field map declared for adapter')

    def _get_val(self, path):
        return reduce(operator.getitem, path.split('.'), self.data)

    def get_address(self, data: dict) -> Address:
        self.data = data
        kwargs = {}
        for key, path in self.field_map.items():
            kwargs[key] = self._get_val(path)

        return Address(**kwargs)


class OSMAdapter(AddressAdapter):
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


# noinspection PyAbstractClass
class AddressSerializer(serializers.Serializer):
    display = serializers.CharField(max_length=500)
    house_nr = serializers.CharField(max_length=20)
    street = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=200)
    # Ref: https://tinyurl.com/max-pc-len
    postal_code = serializers.CharField(max_length=12)
    province = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=200)
    address_type = serializers.CharField(max_length=32)
