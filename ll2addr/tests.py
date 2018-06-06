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
    def get_response(self, lon, lat):
        r = self.client.get(
            '/api/address',
            data={'lon': lon, 'lat': lat}
        )
        self.assertTrue(r.status_code, 200)
        try:
            data = r.json()
        except ValueError:
            raise ValueError(r._body)
        else:
            return data

    def test_uk(self):
        data = self.get_response('-1.81602098644987', '52.5487429714954')
        self.assertTrue('display' in data)
        self.assertEqual(data['display'], "137, Pilkington Avenue, Sutton "
                                          "Coldfield, Birmingham, "
                                          "West Midlands Combined Authority, "
                                          "West Midlands, England, B72 1LH, UK")
        self.assertEqual(data['postal_code'], 'B72 1LH')
        self.assertEqual(data['country'], 'UK')
        self.assertEqual(data['address_type'], 'building')

    def test_nl(self):
        data = self.get_response('6.10918', '53.11214')
        self.assertTrue('display' in data)
        self.assertEqual(data['display'], '23, Bloemkamp, Drachten, '
                                          'Smallingerland, Fryslân, '
                                          'Nederland, 9202CB, Nederland')
        self.assertEqual(data['postal_code'], '9202CB')
        self.assertEqual(data['country'], 'Nederland')

    def test_errors(self):
        # Northpole somehwere in Russia, but not a building, but state boundary
        r = self.client.get(
            '/api/address',
            data={'lon': '58.7167', 'lat': '83.0112'}
        )
        # Even more north, aka not geocodable
        self.assertTrue(r.status_code, 404)
        r = self.client.get(
            '/api/address',
            data={'lon': '58.7167', 'lat': '89.0112'}
        )
        self.assertTrue(r.status_code, 404)
