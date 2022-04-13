from random import choices
from rest_framework import serializers
from products.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class ProductsSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    type_product = serializers.ChoiceField(
        choices=Product.CHOICES_TYPE_PRODUCT)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    commission_percentage = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        model = Product
        fields = ['id', 'bar_code', 'description', 'type_product',
                  'price', 'quantity', 'commission_percentage']

class ProductsItemSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    type_product = serializers.ChoiceField(
        choices=Product.CHOICES_TYPE_PRODUCT)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'description', 'type_product',
                  'price']
