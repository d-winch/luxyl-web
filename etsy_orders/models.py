import os
from datetime import datetime
from html import unescape

from designs.models import Design
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware


class EtsyOrder(models.Model):

    receipt_id = models.IntegerField("Receipt ID", primary_key=True)
    buyer_user_id = models.IntegerField("Buyer ID")
    message_from_buyer = models.TextField("Buyer Message", blank=True, null=True)
    was_paid = models.BooleanField("Is Paid", default=True)
    grandtotal = models.FloatField("Grand Total")
    is_express = models.BooleanField("Is Express", default=False)
    creation_tsz = models.DateTimeField("Order Date")
    downloaded_tsz = models.DateTimeField("Downloaded", auto_now_add=True)
    

    class Meta:
        verbose_name = ("Etsy Order")
        verbose_name_plural = ("Etsy Orders")

    def __str__(self):
        return str(self.receipt_id)
    
    def add_order(receipt):
        order, created = EtsyOrder.objects.update_or_create(
            receipt_id=receipt['receipt_id'],
            defaults={
                'receipt_id': receipt['receipt_id'],
                'buyer_user_id': receipt['buyer_user_id'],
                'message_from_buyer': unescape(receipt['message_from_buyer']) if receipt['message_from_buyer'] else '',
                'was_paid': receipt['was_paid'],
                'is_express': float(receipt['total_shipping_cost'])>0,
                'grandtotal': receipt['grandtotal'],
                'creation_tsz': make_aware(datetime.utcfromtimestamp(receipt['creation_tsz'])),
                'downloaded_tsz': timezone.localtime(timezone.now()),
            },
        )
        return order

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:EtsyOrder_detail", kwargs={"pk": self.pk})


class OrderItem(models.Model):

    transaction_id = models.IntegerField("Transaction ID", primary_key=True)
    title = models.CharField("Item Title", max_length=1024)
    sku = models.CharField("SKU", max_length=50)
    product_id = models.IntegerField("Product ID")
    listing_id = models.IntegerField("Listing ID")
    property_values_size = models.CharField("Size", max_length=12)
    price = models.FloatField("Price")
    quantity = models.IntegerField("Quantity")
    receipt_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("Order Item")
        verbose_name_plural = ("Order Items")

    def __str__(self):
        return self.sku

    def add_order_item(receipt, order):
        design = receipt['product_data']['sku'][0:5]
        order, created = OrderItem.objects.update_or_create(
            transaction_id=receipt['transaction_id'],
            defaults={
                'transaction_id': receipt['transaction_id'],
                'title': unescape(receipt['title']),
                'sku': receipt['product_data']['sku'],
                'product_id': receipt['product_data']['product_id'],
                'listing_id': receipt['listing_id'],
                'property_values_size': unescape(receipt['variations'][0]['formatted_value']),
                'price': receipt['price'],
                'quantity': receipt['quantity'],
                'receipt_id': order,
                'design': Design.objects.filter(pk=design)[0]
            },
        )

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:Product_detail", kwargs={"pk": self.pk})


class CustomerDetail(models.Model):

    buyer_user_id = models.IntegerField("User ID", primary_key=True)
    receipt_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)

    name = models.CharField(
        "Full name",
        max_length=1024,
    )
    
    email = models.EmailField("Buyer Email")

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        null=True,
        blank=True
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )
    
    state = models.CharField(
        "County",
        max_length=1024,
        null=True,
        blank=True
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    country_id = models.IntegerField("Country ID")

    formatted_address = models.TextField(
        "Formatted Address",
        max_length=1024,
    )

    class Meta:
        verbose_name = ("Cutomer Detail")
        verbose_name_plural = ("Cutomer Details")

    def __str__(self):
        return self.name

    def add_customer_detail(receipt, order):
        order, created = CustomerDetail.objects.update_or_create(
            buyer_user_id=receipt['buyer_user_id'],
            defaults={
                'buyer_user_id': receipt['buyer_user_id'],
                'receipt_id': order,
                'name': unescape(receipt['name']) if receipt['name'] else '',
                'email': receipt['buyer_email'],
                'address1': unescape(receipt['first_line']) if receipt['first_line'] else '',
                'address2': unescape(receipt['second_line']) if receipt['second_line'] else '',
                'city': unescape(receipt['city']) if receipt['city'] else '',
                'state': unescape(receipt['state']) if receipt['state'] else '',
                'zip_code': unescape(receipt['zip']) if receipt['zip'] else '',
                'country_id': receipt['country_id'],
                'formatted_address': unescape(receipt['formatted_address']) if receipt['formatted_address'] else '',
            },
        )
        if not created:
            print(receipt)

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:CutomerDetail_detail", kwargs={"pk": self.pk})


class Shipment(models.Model):

    shipping_id = models.IntegerField(primary_key=True)
    receipt_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)
    carrier_name = models.CharField(max_length=50)
    tracking_code = models.CharField(max_length=50)
    tracking_url = models.URLField(blank=True, null=True)
    mailing_date = models.DateTimeField()
    is_express = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Shipment")
        verbose_name_plural = ("Shipments")

    def __str__(self):
        return self.tracking_code
    
    def add_shipping_detail(shipment, order):
        ship, created = Shipment.objects.update_or_create(
            shipping_id=shipment['receipt_shipping_id'],
            defaults={
                'shipping_id': shipment['receipt_shipping_id'],
                'receipt_id': order,
                'carrier_name': unescape(shipment['carrier_name']) if shipment['carrier_name'] else '',
                'tracking_code': shipment['tracking_code'],
                'tracking_url': shipment['tracking_url'],
                'mailing_date': make_aware(datetime.utcfromtimestamp(shipment['mailing_date'])),
                'is_express': getattr(order, 'is_express'),
            },
        )

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:Shipment_detail", kwargs={"pk": self.pk})
