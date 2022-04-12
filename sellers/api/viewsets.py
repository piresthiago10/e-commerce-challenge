from rest_framework import viewsets
from sellers.models import Seller
from sellers.api.serializers import SellersSerializer

class SellersViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellersSerializer