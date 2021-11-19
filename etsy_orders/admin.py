import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import EtsyOrder, CustomerDetail, Product, Shipment

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class CustomerInline(admin.TabularInline):
    model = CustomerDetail
    show_change_link = True
    
class ProductInline(admin.TabularInline):
    model = Product
    show_change_link = True

class ShipmentInline(admin.TabularInline):
    model = Shipment
    show_change_link = True

class EtsyOrderAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = [
        'transaction_id',
        'receipt_id',
        'listing_id',
        'buyer_user_id',
        'was_paid',
        'quantity',
        'message_from_buyer',
        'creation_tsz',
        'paid_tsz',
        'downloaded_tsz'
    ]
    
    actions = ['export_as_csv']

    inlines = [
        CustomerInline,
        ProductInline,
        ShipmentInline,
    ]
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(EtsyOrder, EtsyOrderAdmin)
admin.site.register(CustomerDetail)
admin.site.register(Product)
admin.site.register(Shipment)