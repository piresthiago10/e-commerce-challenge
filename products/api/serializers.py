from random import choices
from rest_framework import serializers
from products.models import Product


class ProductsSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    type_product = serializers.ChoiceField(choices=Product.CHOICES_TYPE_PRODUCT)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    commission_percentage = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id', 'description', 'type_product',
                  'price', 'quantity', 'commission_percentage']
