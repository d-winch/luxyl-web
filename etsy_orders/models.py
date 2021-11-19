from django.db import models
from django.urls import reverse


class EtsyOrder(models.Model):

    transaction_id = models.IntegerField("Transaction ID", primary_key=True)
    quantity = models.IntegerField("Quantity")
    receipt_id = models.IntegerField("Receipt ID")
    listing_id = models.IntegerField("Listing ID")
    buyer_user_id = models.IntegerField("Buyer ID")
    message_from_buyer = models.TextField("Buyer Message", blank=True, null=True)
    was_paid = models.BooleanField("Is Paid", default=True)
    creation_tsz = models.DateTimeField("Created At")
    paid_tsz = models.DateTimeField("Paid At")
    downloaded_tsz = models.DateTimeField("Downloaded At", auto_now_add=True)

    class Meta:
        verbose_name = ("Etsy Order")
        verbose_name_plural = ("Etsy Orders")

    def __str__(self):
        return str(self.transaction_id)

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:EtsyOrder_detail", kwargs={"pk": self.pk})


class Product(models.Model):

    product_id = models.IntegerField("Product ID", primary_key=True)
    title = models.CharField("Item Title", max_length=1024)
    sku = models.CharField("SKU", max_length=50)
    property_values_size = models.CharField("Size", max_length=12)
    price = models.FloatField("Price")
    transaction_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.sku

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:Product_detail", kwargs={"pk": self.pk})


class CustomerDetail(models.Model):

    user_id = models.IntegerField("User ID", primary_key=True)
    transaction_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)

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
        null=True,
        blank=True
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
        verbose_name = ("Cutomer Detail")
        verbose_name_plural = ("Cutomer Details")

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:CutomerDetail_detail", kwargs={"pk": self.pk})


class Shipment(models.Model):

    receipt_shipping_id = models.IntegerField(primary_key=True)
    order_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)
    carrier_name = models.CharField(max_length=50)
    tracking_code = models.CharField(max_length=50)
    mailing_date = models.DateTimeField()

    class Meta:
        verbose_name = ("Shipment")
        verbose_name_plural = ("Shipments")

    def __str__(self):
        return self.tracking_code

    #def get_absolute_url(self):
    #    return reverse("etsy_orders:Shipment_detail", kwargs={"pk": self.pk})
