# Generated by Django 3.0 on 2022-04-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='commission_percentage',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
