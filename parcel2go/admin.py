import base64
import glob
import io
import textwrap
from os.path import dirname, join

from django.contrib import admin
from django.http import HttpResponse
from etsy_orders.models import EtsyOrder
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .models import Parcel2GoShipment


class LabelMixin:
    
    pagesize = (4 * inch, 6 * inch)
    
    def create_picklist_pdf(self, order_details):
        
        x, y = 10, 400
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=self.pagesize)
        
        textobject = can.beginText(x, y)
        textobject.setFont("Helvetica-Oblique", 12)
        
        lines = []
        lines.append("Receipt ID: " + str(order_details.receipt_id))
        lines.append("")
        
        order = EtsyOrder.objects.filter(pk=int(order_details.receipt_id_id)).first()
        customer_detail = order.customerdetail_set.all()[0]
        address = [
            customer_detail.name,
            customer_detail.address1,
            customer_detail.address2,
            customer_detail.city,
            customer_detail.state,
            customer_detail.zip_code
        ]
        lines = lines + [x for x in address if x]
        lines.append("")
        
        for order_item in order.orderitem_set.all():
            wraps = textwrap.wrap(order_item.design.title, 38)
            lines = lines + wraps
            lines.append(f"{order_item.sku}    Qty: {order_item.quantity}")
            lines.append("")
        print(lines)
        
        for line in lines:
            textobject.textLine(line)
        can.drawText(textobject)
        
        img_x, img_y = 10, 10
        for order_item in order.orderitem_set.all():
            png = ImageReader(f"{order_item.design.png}")
            can.rect(img_x, img_y, height=0.8*inch, width=0.8*inch, fill=1)
            can.drawImage(png, img_x, img_y, mask='auto', height=0.8*inch, width=0.8*inch, preserveAspectRatio=True)
            img_x = img_x + 60
            
        can.save()
        packet.seek(0)
        picklist_pdf = PdfFileReader(packet)
        return picklist_pdf
    
    def get_label_pdf(self, request, queryset):
        
        response = HttpResponse(
            content_type="application/pdf",
        )
        response['Content-Disposition'] = 'attachment;filename=labels.pdf'
        
        output = PdfFileWriter()
        for obj in queryset:
            label_bytes = base64.b64decode(obj.label)
            input = PdfFileReader(io.BytesIO(label_bytes))
            picklist = self.create_picklist_pdf(obj)
            output.addPage(input.getPage(0))
            output.addPage(picklist.getPage(0))
        
        outputStream = io.BytesIO()
        output.write(outputStream)
        response.write(outputStream.getvalue())
        return response

    get_label_pdf.short_description = "Get Label(s)"

class Parcel2GoShipmentAdmin(admin.ModelAdmin, LabelMixin):
    list_display = [
        'shipping_line_id',
        'p2g_order_id',
        'receipt_id',
        'carrier_name',
        'tracking_code',
        'order_line_hash',
        'collection_date',
    ]
    
    search_fields = ('shipping_line_id', 'p2g_order_id', 'receipt_id', 'tracking_code',)
    list_filter = ('p2g_order_id', ("tracking_code", admin.EmptyFieldListFilter),)
    
    actions = ['get_label_pdf', 'get_label_pdf2']
    
    # def has_change_permission(self, request, obj=None):
    #     return False

admin.site.register(Parcel2GoShipment, Parcel2GoShipmentAdmin)
