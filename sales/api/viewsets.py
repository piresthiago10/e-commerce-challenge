import imp
from rest_framework import viewsets
from sales.models import Sale, SaleItem
from sales.api.serializers import SalesSerializer, SalesItemsSerializer

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SalesSerializer


class SalesItemsViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SalesItemsSerializer
    