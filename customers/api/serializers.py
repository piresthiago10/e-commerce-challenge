from customers.models import Customer
from django.core.validators import RegexValidator
from rest_framework import serializers


class CustomersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[RegexValidator(regex=r'^[a-zA-Z ]+$')])

    class Meta:
        model = Customer
        fields = ['id', 'name']
