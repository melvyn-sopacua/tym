import operator
from functools import reduce
from . import Address

__all__ = (
    'AddressAdapter',
)


class AddressAdapter(object):
    __doc__ = """
    Base adapter for an Address

    This adapter has two main components:
    - A class-level field map that should map input data keys to Address
    class fields
    - A method py:method`get_address()` that does the actual conversion with the
    given data
    """
    field_map = {}

    def __init__(self):
        self.data = None
        if not self.field_map:
            raise ValueError('No field map declared for adapter')

    def _get_val(self, path):
        return reduce(operator.getitem, path.split('.'), self.data)

    def get_address(self, data) -> Address:
        """
        Take the given input data and return an Address instance representing it

        :param data: Input data, by default this is assumed to be a
            dictionary-like object.
        :return: The address with correct fields mapped to the input data
        """
        self.data = data
        kwargs = {}
        for key, path in self.field_map.items():
            try:
                kwargs[key] = self._get_val(path)
            except KeyError:
                pass

        return Address(**kwargs)
