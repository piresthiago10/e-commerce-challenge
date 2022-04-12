from rest_framework import viewsets
from customers.models import Customer
from customers.api.serializers import CustomersSerializer

class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomersSerializer