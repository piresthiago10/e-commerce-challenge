from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.validators import EmailValidator
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField(validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = Token
        fields = ['token']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']