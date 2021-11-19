# Generated by Django 3.2.9 on 2021-11-18 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_orders', '0005_etsyorder_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='etsyorder',
            name='products',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='etsy_orders.product'),
            preserve_default=False,
        ),
    ]