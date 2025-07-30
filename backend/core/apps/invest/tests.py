import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from apps.invest.models import Company, Country, Market, Sector, Industry, Currency
from django.contrib.auth.models import User


def create_models():
    currency = Currency.objects.create(
        iso_code='test',
        symbol='test',
        name='test',
    )
    country = Country.objects.create(
        iso_code='test',
        currency=currency,
        name='test',
        name_genitive='test',
    )
    Country.objects.create(
        iso_code='test2',
        currency=currency,
        name='test',
        name_genitive='test',
    )
    market = Market.objects.create(
        title='test',
        slug='test',
        country=country,
    )
    sector = Sector.objects.create(
        slug='test',
        title='test',
    )
    industry = Industry.objects.create(
        slug='test',
        sector=sector,
        title='test',
    )
    user = User.objects.create(username='test', date_joined=datetime.datetime.now(datetime.UTC))

    data = {
        'ticker': 'test',
        'slug': 'test',
        'uid': 'test',
        'country': country,
        'market': market,
        'sector': sector,
        'industry': industry,
        'title': 'test',
        'created': datetime.datetime.now(datetime.UTC),
        'updated': datetime.datetime.now(datetime.UTC),
        'created_by': user,
        'updated_by': user,
        'is_visible': True,
    }
    Company.objects.create(**data)
    data2 = {
        'ticker': 'test2',
        'slug': 'test2',
        'uid': 'test2',
        'country': country,
        'market': market,
        'sector': sector,
        'industry': industry,
        'title': 'test',
        'created': datetime.datetime.now(datetime.UTC),
        'updated': datetime.datetime.now(datetime.UTC),
        'created_by': user,
        'updated_by': user,
    }
    Company.objects.create(**data2)


class CompanyListAPITest(APITestCase):
    def test_get_model(self):
        url = '/api/v1/invest/companies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompanyDetailAPITest(APITestCase):
    def setUp(self):
        create_models()

    def tearDown(self):
        pass

    def test_get_model(self):
        url = '/api/v1/invest/companies/test/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_404(self):
        url = '/api/v1/invest/companies/no-existing/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CountryFilterAPITest(APITestCase):
    def test_get_model(self):
        url = '/api/v1/invest/countries/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SectorFilterAPITest(APITestCase):
    def test_get_model(self):
        url = '/api/v1/invest/sectors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CountryOptionsAPITest(APITestCase):
    def test_get_model(self):
        url = '/api/v1/invest/country-options/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CurrencyOptionsAPITest(APITestCase):
    def test_get_model(self):
        url = '/api/v1/invest/currency-options/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PriceDataAPITest(APITestCase):
    def setUp(self):
        create_models()

    def test_get_model(self):
        url = '/api/v1/invest/candles/test/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_404(self):
        url = '/api/v1/invest/candles/no-existing/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SearchQueryAPITest(APITestCase):
    def setUp(self):
        create_models()

    def test_search_query(self):
        url = '/api/v1/invest/search-query/?query=test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ValidateUsernameAPITest(APITestCase):
    def setUp(self):
        create_models()

    def test_username_is_free(self):
        url = '/api/v1/invest/validate-username/?username=free'
        response = self.client.get(url)
        self.assertEqual(response.data.get('isTaken'), False)

    def test_username_is_taken(self):
        url = '/api/v1/invest/validate-username/?username=test'
        response = self.client.get(url)
        self.assertEqual(response.data.get('isTaken'), True)