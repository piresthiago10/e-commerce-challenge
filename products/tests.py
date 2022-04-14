from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from products.models import Product


class ProductTests(APITestCase):
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

    def create_product(self):
        product = Product.objects.create(
            description="Papel A4",
            type_product="product",
            price="22.50",
            quantity=50,
            commission_percentage=4.5
        )
        return product

    def test_create_product(self):
        token = self.get_auth_token()
        url = '/api/products/'
        data = {
            "description": "Papel A5",
            "type_product": "product",
            "price": "25.50",
            "quantity": 30,
            "commission_percentage": 4
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_wrong_type_product(self):
        token = self.get_auth_token()
        url = '/api/products/'
        data = {
            "description": "Papel A5",
            "type_product": "nothing",
            "price": "25.50",
            "quantity": 30,
            "commission_percentage": 4
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_percentage_product(self):
        token = self.get_auth_token()
        url = '/api/products/'
        data = {
            "description": "Papel A5",
            "type_product": "product",
            "price": "25.50",
            "quantity": 30,
            "commission_percentage": 11
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_product(self):
        product = self.create_product()
        token = self.get_auth_token()
        url = f'/api/products/{product.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        product = self.create_product()
        token = self.get_auth_token()
        url = f'/api/products/{product.id}/'
        data = {
            "description": "Papel A5",
            "type_product": "product",
            "price": "25.50",
            "quantity": 30,
            "commission_percentage": 4
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_product(self):
        product = self.create_product()
        token = self.get_auth_token()
        url = f'/api/products/{product.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.delete(url, format='json', **headers)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
