from rest_framework import serializers


__all__ = (
    'AddressSerializer',
)


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
