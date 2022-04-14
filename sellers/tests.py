import datetime
from unittest import mock

from customers.models import Customer
from django.contrib.auth.models import User
from django.urls import reverse
from freezegun import freeze_time
from products.models import Product
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from sales.models import Sale
from sales.tests import SaleTests

from sellers.models import Seller


class SellerTests(APITestCase):
    def create_user(self, username: str) -> object:
        user = User.objects.create(
            username=username,
            email=username+'@teste.com'
        )
        user.set_password(username+'123456')
        user.save()
        return user

    def get_auth_token(self):
        auth_user = self.create_user('token_user')
        token = Token.objects.get_or_create(user=auth_user)
        return token[0]

    def create_seller(self, name):
        seller = Seller.objects.create(
            name=name
        )
        return seller

    def create_customer(self, name):
        customer = Customer.objects.create(
            name=name
        )
        return customer

    def create_product(self, description, price, quantity, commission_percentage, type_product='product'):
        product = Product.objects.create(
            description=description,
            type_product=type_product,
            price=price,
            quantity=quantity,
            commission_percentage=commission_percentage
        )
        return product

    def test_create_seller(self):
        token = self.get_auth_token()
        url = '/api/sellers/'
        data = {'name': 'new seller'}
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_wrong_seller(self):
        token = self.get_auth_token()
        url = '/api/sellers/'
        data = {'name': 'new !@#$%1234'}
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_user(self):
        view_seller = self.create_seller('view_seller')
        token = self.get_auth_token()
        url = f'/api/sellers/{view_seller.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_wrong_user(self):
        token = self.get_auth_token()
        url = f'/api/sellers/100/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_user(self):
        view_seller = self.create_seller('view_seller')
        url = f'/api/sellers/{view_seller.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        view_seller = self.create_seller('view_seller')
        token = self.get_auth_token()
        url = f'/api/sellers/{view_seller.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        data = {'name': 'changed seller'}
        response = self.client.put(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        view_seller = self.create_seller('view_seller')
        token = self.get_auth_token()
        url = f'/api/sellers/{view_seller.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @freeze_time('2013-04-09 01:30:00')
    def test_commission_night(self):
        test_customer_1 = self.create_customer('test_customer_1')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=5.0
        )
        test_product_2 = self.create_product(
            description='test_product_2',
            price="25.00",
            quantity=10,
            commission_percentage=7.0
        )
        test_product_3 = self.create_product(
            description='test_product_3',
            price="40.00",
            quantity=10,
            commission_percentage=4.0
        )
        test_product_4 = self.create_product(
            description='test_product_4',
            price="60.00",
            quantity=10,
            commission_percentage=3.0
        )
        url = '/api/sales/'
        data_1 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        data_2 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_2.pk,
                "quantity": 2
            }]
        }
        data_3 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_3.pk,
                "quantity": 2
            }]
        }
        data_4 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_4.pk,
                "quantity": 1
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        self.client.post(url, data_1, format='json', **headers)
        self.client.post(url, data_2, format='json', **headers)
        self.client.post(url, data_3, format='json', **headers)
        self.client.post(url, data_4, format='json', **headers)
        url = f'/api/comission/seller/{test_seller.pk}/start_date/2013-04-08 00:30:00/end_date/2013-04-10 01:45:00/'
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """
        (10.0 * 0.05) * 5 = 2.5
        (25.0 * 0.05) * 2 = 2.5
        (40.0 * 0.04) * 2 = 3.2
        (60.0 * 0.03) * 1 = 1.8
        """
        self.assertEqual(response.json(), {'comission': 10.0})

    @freeze_time('2013-04-09 14:45:00')
    def test_commission_day(self):
        test_customer_1 = self.create_customer('test_customer_1')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=5.0
        )
        test_product_2 = self.create_product(
            description='test_product_2',
            price="25.00",
            quantity=10,
            commission_percentage=7.0
        )
        test_product_3 = self.create_product(
            description='test_product_3',
            price="40.00",
            quantity=10,
            commission_percentage=2.0
        )
        test_product_4 = self.create_product(
            description='test_product_4',
            price="60.00",
            quantity=10,
            commission_percentage=3.0
        )
        url = '/api/sales/'
        data_1 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        data_2 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_2.pk,
                "quantity": 2
            }]
        }
        data_3 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_3.pk,
                "quantity": 2
            }]
        }
        data_4 = {
            "seller":  test_seller.pk,
            "customer": test_customer_1.pk,
            "items": [{
                "product": test_product_4.pk,
                "quantity": 1
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        self.client.post(url, data_1, format='json', **headers)
        self.client.post(url, data_2, format='json', **headers)
        self.client.post(url, data_3, format='json', **headers)
        self.client.post(url, data_4, format='json', **headers)
        url = f'/api/comission/seller/{test_seller.pk}/start_date/2013-04-08 12:00:01/end_date/2013-04-10 23:59:59/'
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        """
        (10.0 * 0.05) * 5 = 2.5
        (25.0 * 0.07) * 2 = 3.5
        (40.0 * 0.04) * 2 = 3.2
        (60.0 * 0.04) * 1 = 2.4
        """
        self.assertEqual(response.json(), {'comission': 11.6})
