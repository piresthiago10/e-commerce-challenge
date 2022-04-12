from rest_framework import serializers
from sellers.models import Seller

class SellersSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Seller
        fields = ['id', 'name']