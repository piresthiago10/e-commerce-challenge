import imp
from rest_framework import serializers
from sales.models import Sale, SaleItem
from sellers.api.serializers import SellersSerializer
from customers.api.serializers import CustomersSerializer
from products.api.serializers import ProductsSerializer


class SalesSerializer(serializers.ModelSerializer):
    # seller = SellersSerializer(read_only=True)
    # costumer = CustomersSerializer(read_only=True)
    # items = ProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'seller', 'customer', 'items']


class SalesItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'quantity']
