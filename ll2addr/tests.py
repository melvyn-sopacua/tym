from django.test import SimpleTestCase


class AddressViewTest(SimpleTestCase):
    def test_get(self):
        r = self.client.get(
            '/api/address',
            data={'lon': '-1.81602098644987', 'lat': '52.5487429714954'}
        )
        self.assertTrue(r.status_code, 200)
        try:
            data = r.json()
        except ValueError:
            raise ValueError(r._body)
        self.assertTrue('address' in data)
