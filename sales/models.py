import imp
from django.db import models
from sellers.models import Seller
from customers.models import Customer
from products.models import Product
from django.utils import timezone

class Sale(models.Model):
    date = models.DateField(default=timezone.now)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=False, blank=False)
    items = models.ManyToManyField(Product, blank=False)
    quantity = models.IntegerField()
