from rest_framework import viewsets
from customers.models import Customer
from customers.api.serializers import CustomersSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomersSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
