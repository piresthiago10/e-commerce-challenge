# Generated by Django 3.0 on 2022-04-12 22:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20220412_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
