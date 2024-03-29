import csv
from django.utils import timezone, dateformat
from django.contrib import admin
from django.http import HttpResponse
from .models import EtsyOrder, CustomerDetail, OrderItem, Shipment
from parcel2go.models import Parcel2GoShipment

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        timestamp = dateformat.format(timezone.now(), 'Y-m-d H:i:s')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural} - {timestamp}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class CustomerInline(admin.TabularInline):
    model = CustomerDetail
    show_change_link = True
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    show_change_link = True

class ShipmentInline(admin.TabularInline):
    model = Shipment
    show_change_link = True

class Parcel2GoShipmentInline(admin.TabularInline):
    model = Parcel2GoShipment
    show_change_link = True

class CustomerDetailAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        'buyer_user_id',
        'receipt_id',
        'name',
        'email',
        'address1',
        'address2',
        'city',
        'state',
        'zip_code',
        'country_id',
        'formatted_address',
    ]
    
    search_fields = (
        'buyer_user_id',
        'receipt_id__receipt_id',
        'name',
        'email',
        'address1',
        'address2',
        'city',
        'state',
        'zip_code',
        'formatted_address',
    )
    
    readonly_fields=('buyer_user_id', 'receipt_id',)
    
    actions = ['export_as_csv']

class EtsyOrderAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        'receipt_id',
        'buyer_user_id',
        'was_paid',
        'is_express',
        'was_shipped',
        'message_from_buyer',
        'order_items',
        'order_item_count',
        'grandtotal',
        'creation_tsz',
        'downloaded_tsz',
    ]
    
    search_fields = (
        'receipt_id',
        'buyer_user_id',
        'orderitem__sku',
        'message_from_buyer',
    )
    
    ordering = ('-creation_tsz',)
    
    list_filter = ['was_paid', 'creation_tsz']
    actions = ['export_as_csv']

    inlines = [
        CustomerInline,
        OrderItemInline,
        ShipmentInline,
        Parcel2GoShipmentInline,
    ]
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def order_item_count(self, obj):
        return obj.orderitem_set.count()
    order_item_count.short_description = "Item Count"
    
    def order_items(self, obj):
        return "\n".join([o.sku for o in obj.orderitem_set.all()])
    order_items.short_description = "Items"
    
    def was_shipped(self, obj):
        return obj.parcel2goshipment_set.count() > 0
    was_shipped.boolean = True
    was_shipped.short_description = "Shipped"
    

class OrderItemAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        'sku',
        'title',
        'property_values_size',
        'price',
        'quantity',
    ]
    
    actions = ['export_as_csv']
    
    # readonly_fields=('receipt_id', 'transaction_id', 'product_id', 'listing_id')


class ShipmentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        'shipping_id',
        'receipt_id',
        'carrier_name',
        'tracking_code',
        #'tracking_url',
        'mailing_date',
        'is_express',
    ]
    
    list_filter = ['carrier_name', 'mailing_date']
    actions = ['export_as_csv']
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(EtsyOrder, EtsyOrderAdmin)
admin.site.register(CustomerDetail, CustomerDetailAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Shipment, ShipmentAdmin)
