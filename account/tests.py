from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from account.models import APIAccountManager


class APIAccountManagerTests(APITestCase):
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

    def test_create_account(self):
        url = '/api/new_user/'
        data = {'username': 'user_one', 'password': '123456',
                'email': 'user_one@teste.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_user(self):
        auth_user = self.create_user('auth_user')
        url = reverse('login')
        data = {'username': auth_user.username,
                'password': 'auth_user'+'123456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_auth_user(self):
        url = reverse('login')
        data = {'username': 'wrong_user', 'password': 'wrong_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_user(self):
        view_user = self.create_user('view_user')
        token = self.get_auth_token()
        url = f'/api/accounts/{view_user.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_view_user(self):
        view_user = self.create_user('view_user')
        url = f'/api/accounts/{view_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):
        view_user = self.create_user('view_user')
        token = self.get_auth_token()
        url = f'/api/accounts/{view_user.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        data = {'username': 'new_username', 'email': view_user.email,
                'password': 'view_user'+'123456'}
        response = self.client.put(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        view_user = self.create_user('view_user')
        token = self.get_auth_token()
        url = f'/api/accounts/{view_user.id}/'
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}
        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
