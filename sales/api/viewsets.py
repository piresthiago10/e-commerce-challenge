import imp
from rest_framework import viewsets
from sales.models import Sale
from sales.api.serializers import SalesSerializer

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SalesSerializer