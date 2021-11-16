# Generated by Django 3.2.9 on 2021-11-16 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CutomerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Full name')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('country_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'CutomerDetail',
                'verbose_name_plural': 'CutomerDetails',
            },
        ),
        migrations.CreateModel(
            name='EtsyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('receipt_id', models.IntegerField()),
                ('listing_id', models.IntegerField()),
                ('buyer_user_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('sku', models.TextField(blank=True, null=True)),
                ('property_values_size', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('message_from_buyer', models.TextField(blank=True, null=True)),
                ('was_paid', models.BooleanField(default=True)),
                ('buyer_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('credit', models.FloatField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_tsz', models.DateTimeField()),
                ('paid_tsz', models.DateTimeField()),
                ('shipped_tsz', models.DateTimeField()),
                ('downloaded_tsz', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'EtsyOrder',
                'verbose_name_plural': 'EtsyOrders',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_shipping_id', models.IntegerField()),
                ('carrier_name', models.TextField(blank=True, null=True)),
                ('tracking_code', models.TextField(blank=True, null=True)),
                ('mailing_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Shipment',
                'verbose_name_plural': 'Shipments',
            },
        ),
    ]