# Generated by Django 3.2.9 on 2021-11-16 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('title', models.TextField(blank=True, null=True)),
                ('sku', models.TextField(blank=True, null=True)),
                ('property_values_size', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.RemoveField(
            model_name='etsyorder',
            name='buyer_email',
        ),
        migrations.RemoveField(
            model_name='etsyorder',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='etsyorder',
            name='is_active',
        ),
    ]