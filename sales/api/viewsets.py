from products.models import Product
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sales.api.serializers import (SalesDetailSerializer, SalesItemsSerializer,
                                   SalesSerializer)
from sales.models import Sale, SaleItem


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SalesSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data

        items = data.get('items')

        items_to_save = []
        for item in items:
            item_serializer = SalesItemsSerializer(data=item)
            if item_serializer.is_valid(raise_exception=True):
                product = item_serializer.validated_data.get('product')
                quantity = item_serializer.validated_data.get('quantity')
                if not product.verify_product_quantity(product, quantity):
                    return Response({'message': 'Quantity in stock is not enough.'}, status=status.HTTP_400_BAD_REQUEST)
                items_to_save.append(item_serializer.validated_data)

        sale_items = []
        for item in items_to_save:
            product = item.get('product')
            quantity = item.get('quantity')
            sale_item = SaleItem.objects.create(
                product=product,
                quantity=quantity)
            product.decrease_quantity(quantity)
            sale_items.append(sale_item)

        sales_serializer = SalesSerializer(data=data)
        if sales_serializer.is_valid(raise_exception=True):
            seller = sales_serializer.validated_data.get('seller')
            customer = sales_serializer.validated_data.get('customer')
            sale = Sale.objects.create(seller=seller, customer=customer)
            sale.items.set(sale_items)

        detail_serializer = SalesDetailSerializer(sale)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class SalesDetailViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SalesDetailSerializer
    http_method_names = ['get']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class SalesItemsViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SalesItemsSerializer
    http_method_names = ['get', 'post']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
