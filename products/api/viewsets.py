from rest_framework import viewsets
from products.models import Product
from products.api.serializers import ProductsSerializer

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer