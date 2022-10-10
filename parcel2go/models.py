from datetime import datetime
from html import unescape

from django.db import models
from django.utils.timezone import make_aware
from etsy_orders.models import EtsyOrder


class Parcel2GoShipment(models.Model):

    shipping_line_id = models.CharField(max_length=100, primary_key=True)
    p2g_order_id = models.CharField(max_length=50)
    receipt_id = models.ForeignKey(EtsyOrder, on_delete=models.CASCADE)
    carrier_name = models.CharField(max_length=50, null=True, blank=True)
    tracking_code = models.CharField(max_length=50, null=True, blank=True)
    order_line_hash = models.CharField(max_length=50)
    order_hash = models.CharField(max_length=50)
    collection_date = models.DateTimeField()
    label = models.TextField()

    class Meta:
        verbose_name = ("Shipment")
        verbose_name_plural = ("Shipments")

    def __str__(self):
        return self.shipping_line_id
    
    def add_shipping_detail(order_line, order_id, carrier_name, order_hash, collection_date):
        etsy_reference = order_line["ItemId"].replace("00000000-0000-0000-0000-00","")
        ship, created = Parcel2GoShipment.objects.update_or_create(
            shipping_line_id=order_line["OrderLineId"],
            defaults={
                'shipping_line_id': order_line["OrderLineId"],
                'p2g_order_id': order_id,
                'receipt_id': EtsyOrder.objects.get(pk=etsy_reference),
                'carrier_name': carrier_name,
                'tracking_code': None,
                'order_line_hash': order_line["Hash"],
                'order_hash': order_hash,
                'collection_date': collection_date,
            },
        )
