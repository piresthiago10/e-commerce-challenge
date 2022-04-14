from customers.models import Customer
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from sellers.models import Seller

from sales.models import Sale


class SaleTests(APITestCase):
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

    def test_create_sale(self):
        test_customer = self.create_customer('test_customer')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        test_product_2 = self.create_product(
            description='test_product_2',
            price="20.00",
            quantity=10,
            commission_percentage=1.5
        )
        test_product_3 = self.create_product(
            description='test_product_3',
            price="30.00",
            quantity=10,
            commission_percentage=7.3
        )
        test_product_4 = self.create_product(
            description='test_product_4',
            price="40.00",
            quantity=10,
            commission_percentage=6.5
        )
        test_product_5 = self.create_product(
            description='test_product_5',
            price="50.00",
            quantity=10,
            commission_percentage=2.0
        )
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 6
            }, {
                "product": test_product_2.pk,
                "quantity": 5
            }, {
                "product": test_product_3.pk,
                "quantity": 8
            }, {
                "product": test_product_4.pk,
                "quantity": 2
            }, {
                "product": test_product_5.pk,
                "quantity": 1
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_quantity_greater_than_stock_sale(self):
        test_customer = self.create_customer('test_customer')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 11
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_wrong_pk_sale(self):
        test_customer = self.create_customer('test_customer')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": 867,
                "quantity": 5
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_seller_pk_sale(self):
        test_customer = self.create_customer('test_customer')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        url = '/api/sales/'
        data = {
            "seller":  789,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_customer_pk_sale(self):
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": 453,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_sale(self):
        test_customer = self.create_customer('test_customer')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        last_sale = Sale.objects.last()
        url = f'/api/sales/{last_sale.pk}/'
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_sale(self):
        test_customer = self.create_customer('test_customer')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        test_product_2 = self.create_product(
            description='test_product_2',
            price="20.00",
            quantity=10,
            commission_percentage=1.0
        )
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        last_sale = Sale.objects.last()
        url = f'/api/sales/{last_sale.pk}/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_2.pk,
                "quantity": 5
            }]
        } 
        response = self.client.put(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_sale(self):
        test_customer = self.create_customer('test_customer')
        test_seller = self.create_seller('test_seller')
        test_token = self.get_auth_token()
        test_product_1 = self.create_product(
            description='test_product_1',
            price="10.00",
            quantity=10,
            commission_percentage=1.0
        )
        url = '/api/sales/'
        data = {
            "seller":  test_seller.pk,
            "customer": test_customer.pk,
            "items": [{
                "product": test_product_1.pk,
                "quantity": 5
            }]
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(test_token)}
        response = self.client.post(url, data, format='json', **headers)
        last_sale = Sale.objects.last()
        url = f'/api/sales/{last_sale.pk}/'
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)