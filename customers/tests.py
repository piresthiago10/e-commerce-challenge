from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from customers.models import Customer


class CustomerTests(APITestCase):
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

    def create_customer(self, name):
        customer = Customer.objects.create(
            name=name
        )
        return customer

    def test_create_customer(self):
        token = self.get_auth_token()
        url = '/api/customers/'
        data = {'name': 'new customer'}
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_wrong_customer(self):
        token = self.get_auth_token()
        url = '/api/customers/'
        data = {'name': 'new !@#$%1234'}
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_user(self):
        view_customer = self.create_customer('view_customer')
        token = self.get_auth_token()
        url = f'/api/customers/{view_customer.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_wrong_user(self):
        token = self.get_auth_token()
        url = f'/api/customers/100/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_view_user(self):
        view_customer = self.create_customer('view_customer')
        url = f'/api/customers/{view_customer.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        view_customer = self.create_customer('view_customer')
        token = self.get_auth_token()
        url = f'/api/customers/{view_customer.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        data = {'name': 'changed customer'}
        response = self.client.put(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        view_customer = self.create_customer('view_customer')
        token = self.get_auth_token()
        url = f'/api/customers/{view_customer.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
