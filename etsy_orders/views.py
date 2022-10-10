from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
import pytz
from .etsy import EtsyClient
from .models import EtsyOrder
from .google_sheets import orders_to_sheets

def index(request):
    context = {"context": "hello"}
    return render(request, 'index.html', context)

def order(request, order_id):
    context = {"context": "order"}
    return render(request, 'index.html', context)

def get_orders(request):
    limit = int(request.GET.get('limit', 1))
    offset = int(request.GET.get('offset', 0))
    etsy = EtsyClient()
    #transactions = etsy.process_orders(limit=25, offset=0)
    etsy.process_shop_receipts(limit=limit, offset=offset, was_paid=True, was_shipped=False)
    context = {"context": ''}
    return render(request, 'index.html', context)

def orders_to_appsheet(request):
    # Get orders from etsy
    limit = int(request.GET.get('limit', 1))
    offset = int(request.GET.get('offset', 0))
    was_paid = bool(request.GET.get('was_paid', True))
    was_shipped = bool(request.GET.get('was_shipped', False))
    etsy = EtsyClient()
    etsy.process_shop_receipts(limit=limit, offset=offset, was_paid=was_paid, was_shipped=was_shipped)
    
    # Add unshipped orders to Google Sheet
    unshipped = EtsyOrder.objects.filter(shipment__isnull=True)
    orders_to_sheets(orders=unshipped)
    context = {"context": unshipped}
    return render(request, 'index.html', context)