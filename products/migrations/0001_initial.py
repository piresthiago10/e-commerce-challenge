# Generated by Django 3.0 on 2022-04-12 05:29

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bar_code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('description', models.CharField(max_length=140)),
                ('type_product', models.CharField(choices=[('product', 'Produto'), ('service', 'Serviço')], default='product', max_length=7)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('commission_percentage', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
        ),
    ]
