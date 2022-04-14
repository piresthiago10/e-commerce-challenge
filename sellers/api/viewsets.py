from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sales.models import Sale
from sellers.api.serializers import SellersSerializer
from sellers.models import Seller


class SellersViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellersSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]