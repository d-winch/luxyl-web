# Generated by Django 3.2.9 on 2021-11-18 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_orders', '0006_etsyorder_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etsyorder',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='etsyorder',
            name='products',
        ),
    ]