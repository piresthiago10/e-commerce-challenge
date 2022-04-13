from django.core.validators import RegexValidator
from rest_framework import serializers
from sellers.models import Seller


class SellersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[RegexValidator(regex=r'^[a-zA-Z ]+$')])

    class Meta:
        model = Seller
        fields = ['id', 'name']


class SellerComissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    start_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    end_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Seller
        fields = ['id', 'start_date', 'end_date']
