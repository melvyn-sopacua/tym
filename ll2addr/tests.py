from django.test import SimpleTestCase
from ll2addr.serializers import OSMAdapter, Address
import json


class AdapterTest(SimpleTestCase):
    adapter = OSMAdapter()
    osm_data = '{"place_id":"91015268","licence":"Data © OpenStreetMap ' \
               'contributors, ODbL 1.0. https:\/\/osm.org\/copyright",' \
               '"osm_type":"way","osm_id":"90394420","lat":"52.54877605",' \
               '"lon":"-1.81627033283164","place_rank":"30","category":' \
               '"building","type":"yes","importance":"0","addresstype":' \
               '"building","name":null,"display_name":"137, Pilkington ' \
               'Avenue, Sutton Coldfield, Birmingham, West Midlands Combined ' \
               'Authority, West Midlands, England, B72 1LH, UK","address":{' \
               '"house_number":"137","road":"Pilkington Avenue","town":' \
               '"Sutton Coldfield","city":"Birmingham","county":"West ' \
               'Midlands Combined Authority","state_district":"West ' \
               'Midlands","state":"England","postcode":"B72 1LH","country":' \
               '"UK","country_code":"gb"},"boundingbox":["52.5487321",' \
               '"52.5488299","-1.8163514","-1.8161885"]}'

    def test_osm(self):
        data = json.loads(self.osm_data)
        address = self.adapter.get_address(data)
        self.assertIsInstance(address, Address)
        self.assertEqual(address.city, 'Birmingham')
        self.assertEqual(address.postal_code, 'B72 1LH')
        self.assertEqual(address.country, 'UK')


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
        self.assertTrue('display' in data)
        self.assertEqual(data['display'], "137, Pilkington Avenue, Sutton "
                                          "Coldfield, Birmingham, "
                                          "West Midlands Combined Authority, "
                                          "West Midlands, England, B72 1LH, UK")
        self.assertEqual(data['postal_code'], 'B72 1LH')
        self.assertEqual(data['country'], 'UK')
        self.assertEqual(data['address_type'], 'building')
