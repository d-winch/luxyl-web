from django.db import models
from django.urls import reverse


class EtsyOrder(models.Model):

    transaction_id = models.IntegerField("Transaction ID")
    quantity = models.IntegerField("Quantity")
    receipt_id = models.IntegerField("Receipt ID")
    listing_id = models.IntegerField("Listing ID")
    buyer_user_id = models.IntegerField("Buyer ID")

    message_from_buyer = models.TextField(
        "Buyer Message", blank=True, null=True)
    was_paid = models.BooleanField("Is Paid", default=True)

    creation_tsz = models.DateTimeField("Created At")
    paid_tsz = models.DateTimeField("Paid At")

    downloaded_tsz = models.DateTimeField("Downloaded At", auto_now_add=True)

    class Meta:
        verbose_name = ("EtsyOrder")
        verbose_name_plural = ("EtsyOrders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("EtsyOrder_detail", kwargs={"pk": self.pk})


class Product(models.Model):

    product_id = models.IntegerField("Product ID")
    title = models.TextField("Item Title", blank=True, null=True)
    sku = models.TextField("SKU", blank=True, null=True)
    property_values_size = models.TextField("Size", blank=True, null=True)
    price = models.FloatField("Price")

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class CutomerDetail(models.Model):

    name = models.CharField(
        "Full name",
        max_length=1024,
    )

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    country_id = models.IntegerField("Country ID")

    formatted_address = models.CharField(
        "Formatted Address",
        max_length=1024,
    )

    class Meta:
        verbose_name = ("CutomerDetail")
        verbose_name_plural = ("CutomerDetails")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("CutomerDetail_detail", kwargs={"pk": self.pk})


class Shipment(models.Model):

    receipt_shipping_id = models.IntegerField()
    carrier_name = models.TextField(blank=True, null=True)
    tracking_code = models.TextField(blank=True, null=True)
    mailing_date = models.DateTimeField()

    class Meta:
        verbose_name = ("Shipment")
        verbose_name_plural = ("Shipments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Shipment_detail", kwargs={"pk": self.pk})
