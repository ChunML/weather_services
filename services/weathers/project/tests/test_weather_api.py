import json
import unittest
from project import db
from project.api.models import Weather
from project.tests.base import BaseTestCase
from faker import Faker
from datetime import datetime
import re


def add_dummy_data(city=None, date=None,
                   max_temp=None, min_temp=None,
                   wind=None, rain=None, daylight=None):
    fake = Faker()
    weather = Weather(
        city=city or fake.city(),
        date=date or fake.past_date(),
        max_temp=max_temp or fake.pyfloat(2),
        min_temp=min_temp or fake.pyfloat(2),
        wind=wind or fake.pyfloat(2),
        rain=rain or fake.pyfloat(2),
        daylight=daylight or fake.pyfloat(2))
    db.session.add(weather)
    db.session.commit()

    return weather


class TestWeatherApi(BaseTestCase):
    def test_get_weathers(self):
        add_dummy_data()
        add_dummy_data()
        response = self.client.get('/weathers/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertEqual(len(data['data']), 2)
        for i in range(2):
            self.assertTrue(isinstance(data['data'][i]['city'], str))
            self.assertTrue(isinstance(data['data'][i]['date'], str))
            self.assertTrue(isinstance(data['data'][i]['min_temp'], float))
            self.assertTrue(isinstance(data['data'][i]['max_temp'], float))
            self.assertTrue(isinstance(data['data'][i]['wind'], float))
            self.assertTrue(isinstance(data['data'][i]['rain'], float))
            self.assertTrue(isinstance(data['data'][i]['daylight'], float))

    def test_get_weathers_date(self):
        add_dummy_data(date=datetime(2019, 1, 1))
        add_dummy_data(date=datetime(2019, 2, 10))
        add_dummy_data(date=datetime(2018, 3, 11))
        add_dummy_data(date=datetime(2018, 3, 21))
        response = self.client.get('/weathers/date/2019/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertEqual(len(data['data']), 2)
        for i in range(2):
            self.assertIsNotNone(re.match('^2019/[0-9]{2}/[0-9]{2}$', data['data'][i]['date']))

        response = self.client.get('/weathers/date/2018-3/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertEqual(len(data['data']), 2)
        for i in range(2):
            self.assertIsNotNone(re.match('^2018/03/[0-9]{2}$', data['data'][i]['date']))

        response = self.client.get('/weathers/date/2019-02-10/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertEqual(len(data['data']), 1)
        self.assertEqual('2019/02/10', data['data'][0]['date'])

    def test_get_weathers_city(self):
        add_dummy_data(city='Yokohama',
                       date=datetime(2018, 4, 1))
        add_dummy_data(city='Tokyo',
                       date=datetime(2018, 5, 11))
        response = self.client.get('/weathers/city/Yokohama/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertEqual(data['data'][0]['city'], 'Yokohama')
        self.assertEqual(data['data'][0]['date'], '2018/04/01')

        response = self.client.get('/weathers/city/Tokyo/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data'][0]['city'], 'Tokyo')
        self.assertEqual(data['data'][0]['date'], '2018/05/11')

    def test_get_weathers_date_city(self):
        add_dummy_data(city='Yokohama',
                       date=datetime(2018, 4, 1))
        add_dummy_data(city='Yokohama',
                       date=datetime(2018, 4, 22))
        add_dummy_data(city='Yokohama',
                       date=datetime(2018, 5, 11))
        response = self.client.get('/weathers/date/2018/Yokohama/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 3)
        self.assertIn('success', data['status'])
        self.assertEqual(data['data'][0]['city'], 'Yokohama')
        self.assertEqual(data['data'][0]['date'], '2018/04/01')
        self.assertEqual(data['data'][1]['city'], 'Yokohama')
        self.assertEqual(data['data'][1]['date'], '2018/04/22')
        self.assertEqual(data['data'][2]['city'], 'Yokohama')
        self.assertEqual(data['data'][2]['date'], '2018/05/11')

        response = self.client.get('/weathers/date/2018-4/Yokohama/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 2)
        self.assertIn('success', data['status'])
        self.assertEqual(data['data'][0]['city'], 'Yokohama')
        self.assertEqual(data['data'][0]['date'], '2018/04/01')
        self.assertEqual(data['data'][1]['city'], 'Yokohama')
        self.assertEqual(data['data'][1]['date'], '2018/04/22')

        response = self.client.get('/weathers/date/2018-5-11/Yokohama/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 1)
        self.assertIn('success', data['status'])
        self.assertEqual(data['data'][0]['city'], 'Yokohama')
        self.assertEqual(data['data'][0]['date'], '2018/05/11')