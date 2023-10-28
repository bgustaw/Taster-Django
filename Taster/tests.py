from unittest import TestCase

from .models import Country


class CountryTestCase(TestCase):
    def setUp(self):
        Country.objects.create(country=1, continent='Europe', alpha2_code='ts')
        Country.objects.create(country="Poland", continent='Europe', alpha2_code='pl')

    def test_country_in_Europe(self):
        poland = Country.objects.get(alpha2_code='pl')
        testistan = Country.objects.get(alpha2_code='ts')
        self.assertEqual(testistan.continent, 'Europe')
        self.assertEqual(poland.continent, 'Europe')


