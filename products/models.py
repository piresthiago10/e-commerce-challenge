import uuid
from django.db import models

class Product(models.Model):
    CHOICES_TYPE_PRODUCT = (
        ('product', 'Produto'),
        ('service', 'Serviço'),
    )

    bar_code = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=140)
    type_product = models.CharField(max_length=7, choices=CHOICES_TYPE_PRODUCT, default='product')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    commission_percentage = models.DecimalField(max_digits=3, decimal_places=1)

    def verify_product_quantity(self, quantity: int) -> bool:
        return not self.quantity > quantity

    def decrease_quantity(self, quantity:int) -> None:
        self.quantity -= quantity
        
        return self.save()

    def __str__(self):
        return self.description
