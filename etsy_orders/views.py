from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
import pytz
from .etsy import EtsyClient
from .models import EtsyOrder

def index(request):
    context = {"context": "hello"}
    return render(request, 'index.html', context)

def order(request, order_id):
    context = {"context": "order"}
    return render(request, 'index.html', context)

def get_orders(request):
    etsy = EtsyClient()
    transactions = etsy.get_transactions(limit=500, offset=700)
    
    for transaction in transactions:
        print(transaction['transaction_id'])
        
        obj, created = EtsyOrder.objects.update_or_create(
            transaction_id=transaction['transaction_id'],
            defaults={
                'transaction_id': transaction['transaction_id'],
                'quantity': transaction['quantity'],
                'receipt_id': transaction['receipt_id'],
                'listing_id': transaction['listing_id'],
                'buyer_user_id': transaction['buyer_user_id'],
                #message_from_buyer: transaction['message_from_buyer'],
                #was_paid: transaction['was_paid'],
                'paid_tsz': make_aware(datetime.utcfromtimestamp(transaction['paid_tsz'])),
                'creation_tsz': make_aware(datetime.utcfromtimestamp(transaction['creation_tsz'])),
                'downloaded_tsz': timezone.localtime(timezone.now()),
            },
        )
        print(created)
    print(len(transactions))
    
    context = {"context": transactions}
    return render(request, 'index.html', context)