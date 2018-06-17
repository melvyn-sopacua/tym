__all__ = (
    'Address',
)


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
