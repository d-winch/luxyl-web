# Generated by Django 3.2.9 on 2021-11-18 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_orders', '0003_rename_cutomerdetail_customerdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetail',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2'),
        ),
    ]
