import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
    commission_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.description
