from rest_framework import serializers
from customers.models import Customer

class CustomersSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Customer
        fields = ['id', 'name']