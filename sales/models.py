import imp
from datetime import datetime
from itertools import product

from customers.models import Customer
from django.db import models
from django.utils import timezone
from products.models import Product
from sellers.models import Seller


class SaleItem(models.Model):
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False)
    quantity = models.IntegerField()


class Sale(models.Model):
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=False, blank=False)
    items = models.ManyToManyField(SaleItem, blank=False)

    def items_comission_value(self, item: object) -> int:
        item_sale_date = item.get('date').time()
        product = Product.objects.get(id=item.get('product_id'))
        price = product.price
        commission_percentage = 0
        comission = 0

        # Em vendas ocorridas entre 00:00 e 12:00 a comissão de cada item dev ser no máximo 5%;
        start_time = datetime.strptime('00:00:00', '%H:%M:%S').time()
        end_time = datetime.strptime('12:00:00', '%H:%M:%S').time()

        if item_sale_date >= start_time and item_sale_date <= end_time:
            if product.commission_percentage > 5:
                commission_percentage = 5
            else:
                commission_percentage = product.commission_percentage  

        # Em vendas ocorridas entre 12:00:01 e 23:59:59 a comissão de cada item deve ser no mínimo 4%
        start_time = datetime.strptime('12:00:01', '%H:%M:%S').time()
        end_time = datetime.strptime('23:59:59', '%H:%M:%S').time()
        if item_sale_date >= start_time and item_sale_date <= end_time:
            if product.commission_percentage < 4:
                commission_percentage = 4
            else:
                commission_percentage = product.commission_percentage 

        percentage = float(commission_percentage) / 100.0
        comission = (float(price) * percentage) * item.get('quantity')
        
        return round(comission, 2)

    def calculate_commission(self, seller: int, start_date: datetime, end_date: datetime):
        sales = Sale.objects.filter(seller=seller).filter(date__gte=start_date, date__lte=end_date)
        comissions = []
        
        for sale in sales:
            for item in sale.items.values():
                comissions.append(self.items_comission_value(item))

        return sum(comissions)

