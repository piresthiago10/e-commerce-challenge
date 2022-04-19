from django.db.models import Q
from products.api.serializers import (ProductSearchSerializer,
                                      ProductsSerializer)
from products.models import Product
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    http_method_names = ['get', 'post']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:    
            return Product.objects.filter(Q(description__contains=search) | Q(bar_code__contains=search))
        return Product.objects.all()
    
