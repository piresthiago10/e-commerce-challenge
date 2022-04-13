from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from sales.models import Sale

from sellers.api.serializers import SellerComissionSerializer
from sellers.models import Seller


class SellersComission(generics.GenericAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerComissionSerializer

    def get(self, request, *args, **kwargs):
        serializer = SellerComissionSerializer(data=kwargs)
        if serializer.is_valid():
            data = serializer.validated_data
            sale = Sale()
            comission = sale.calculate_commission(data['id'], data['start_date'], data['end_date'])
            return Response({'comission': comission}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
