import imp
from itertools import product

from customers.api.serializers import CustomersSerializer
from customers.models import Customer
from products.api.serializers import ProductsItemSerializer, ProductsSerializer
from products.models import Product
from rest_framework import serializers
from sales.models import Sale, SaleItem
from sellers.api.serializers import SellersSerializer
from sellers.models import Seller


class SalesItemsSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'quantity']

class SalesDetailItemsSerializer(serializers.ModelSerializer):
    product = ProductsItemSerializer(read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'quantity']

class SalesSerializer(serializers.ModelSerializer):

    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
        
    class Meta:
        model = Sale
        fields = ['seller', 'customer']

class SalesDetailSerializer(serializers.ModelSerializer):
    seller = SellersSerializer(read_only=True)
    customer = CustomersSerializer(read_only=True)
    items = SalesDetailItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'seller', 'customer', 'items']
