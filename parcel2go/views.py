import pprint
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import make_aware
from etsy_orders.etsy import EtsyClient
from etsy_orders.models import CustomerDetail, EtsyOrder

from parcel2go.address import Address

from .models import Parcel2GoShipment
from .p2g import P2G, P2GSandbox
from .parcel import Item, Parcel

pp = pprint.PrettyPrinter(indent=4)


def index(request):
    unshipped_orders = EtsyOrder.objects.filter(
        Q(shipment__isnull=True) &
        ~Q(customerdetail__formatted_address__icontains="Northern Ireland") &
        ~Q(customerdetail__formatted_address__icontains="Jersey") &
        ~Q(customerdetail__formatted_address__icontains="Guernsey")
    )
    for t in unshipped_orders:
        print(t.customerdetail_set.all()[0].formatted_address)
    context = {"context": unshipped_orders}
    return render(request, 'index.html', context)


def verify_shipping(request):
    
    carrier = str(request.GET.get('carrier'))
    
    unshipped_orders = EtsyOrder.objects.filter(
        Q(shipment__isnull=True) &
        ~Q(customerdetail__formatted_address__icontains="Northern Ireland") &
        ~Q(customerdetail__formatted_address__icontains="Jersey") &
        ~Q(customerdetail__formatted_address__icontains="Guernsey") &
        ~Q(customerdetail__zip_code__istartswith="BT")
    )

    addresses = []
    parcels = []

    for order in unshipped_orders:
        print(order)

        customer = order.customerdetail_set.all()[0]

        address = Address(
            contact_name=customer.name,
            email=customer.email,
            phone=" ",
            property=" ",
            street=f"{customer.address1} {customer.address2}".strip(),
            town=customer.city,
            county=customer.state,
            postcode=customer.zip_code,
            country_iso_code="GBR",
            country_id=0
        )

        items = []
        for item in order.orderitem_set.all():
            order_item = Item(
                name="Hoodie" if "JH001" in item.sku else "T-Shirt",
                unit_price=item.price,
                weight_kg=0.5 if "JH001" in item.sku else 0.15,
                length=30,
                width=23,
                height=7 if "JH001" in item.sku else 3,
                qty=item.quantity
            )
            items.append(order_item)
        # TODO: Check if receipt ID is correct, or if transaction ID is needed
        parcel = Parcel(parcel=items, etsy_reference=order.receipt_id)
        print()
        print(parcel.total_parcel_cost, parcel.total_items,
              parcel.weight_kg, parcel.dimensions, parcel.contents)
        print(address)
        print()

        addresses.append(address)
        parcels.append(parcel)

    collection_date = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0)
    if datetime.now().hour > 12:
        collection_date = collection_date + timedelta(days=1, hours=12)
    collection_date = collection_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    print(carrier)
    p2g = P2G()
    verified = p2g.verify_order(
        addresses=addresses, parcels=parcels, collection_date=collection_date, service_slug=carrier)
    pp.pprint(verified.json())
    print("Cost:", verified.json()["Cost"])
    print("Errors:", verified.json()["Errors"])

    #context = {"context": [order.receipt_id for order in unshipped_orders]}
    context = {"verified": verified.json()}
    return render(request, 'pages/verify.html', context=context)


def create_order(request):
    
    carrier = str(request.GET.get('carrier'))
    unshipped_orders = EtsyOrder.objects.filter(
        parcel2goshipment__isnull=True).filter(is_express=False)
    if not unshipped_orders:
        return JsonResponse({'message': 'No unshipped orders'})

    addresses = []
    parcels = []

    for order in unshipped_orders:
        print(order)
        customer = order.customerdetail_set.all()[0]

        address = Address(
            contact_name=customer.name,
            email=customer.email,
            phone=" ",
            property=" ",
            street=f"{customer.address1} {customer.address2}".strip(),
            town=customer.city,
            county=customer.state,
            postcode=customer.zip_code,
            country_iso_code="GBR",
            country_id=0
        )

        items = []
        for item in order.orderitem_set.all():
            order_item = Item(
                name="Hoodie" if "JH001" in item.sku else "T-Shirt",
                unit_price=item.price,
                weight_kg=0.5 if "JH001" in item.sku else 0.15,
                length=30,
                width=23,
                height=7 if "JH001" in item.sku else 3,
                qty=item.quantity
            )
            items.append(order_item)
        # TODO: Check if receipt ID is correct, or if transaction ID is needed
        parcel = Parcel(parcel=items, etsy_reference=order.receipt_id)
        print()
        print(parcel.total_parcel_cost, parcel.total_items,
              parcel.weight_kg, parcel.dimensions, parcel.contents)
        print(address)
        print()

        addresses.append(address)
        parcels.append(parcel)

    collection_date = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0)
    if datetime.now().hour > 12:
        collection_date = collection_date + timedelta(days=1, hours=12)
    collection_date = collection_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    print(carrier)
    p2g = P2G()
    created_order = p2g.create_order(
        addresses=addresses, parcels=parcels, collection_date=collection_date, service_slug=carrier)

    pp.pprint(created_order.json())

    if "Errors" in created_order.json():
        return JsonResponse(created_order.json())

    order_id = created_order.json()["OrderId"]
    order_hash = created_order.json()["Hash"]
    
    for order_line in created_order.json()["OrderlineIdMap"]:
        
        Parcel2GoShipment.add_shipping_detail(
            order_line, order_id, carrier, order_hash, collection_date)

    payment_link = created_order.json()['Links']['payment']
    print(order_id)
    context = {
        "payment_link": payment_link,
        "order_id": order_id
    }
    return render(request, 'pages/index.html', context=context)


def labels_tracking(request):
    
    order_id = str(request.GET.get('order_id'))
    submit_to_etsy = int(request.GET.get('submit_to_etsy', 0))
    print(bool(submit_to_etsy))
    
    untracked_parcels = Parcel2GoShipment.objects.filter(
        p2g_order_id=int(order_id))
    print(untracked_parcels)
    if not untracked_parcels:
        return JsonResponse({'message': 'No orders without tracking'})

    p2g = P2G()
    etsy = EtsyClient()
    labels = p2g.get_labels(order_id=order_id, detail="Labels",
                            media="Label4x6", label_format="PDF").json()
    pp.pprint(labels)
    for label in labels['Items']:
        try:
            obj, created = Parcel2GoShipment.objects.update_or_create(
                shipping_line_id=str(label['OrderLineId']),
                defaults={
                    'tracking_code': str(label['CourierTrackingNumbers'][0]),
                    'label': label['Base64EncodedLabel']
                },
        )
        except Exception as e:
            print(e)
    tracked_parcels = Parcel2GoShipment.objects.filter(
        p2g_order_id=int(order_id))
    
    if submit_to_etsy:
        for parcel in tracked_parcels:
            try:
                tracked = etsy.submit_tracking(receipt_id=parcel.receipt_id.receipt_id,
                                        tracking_code=parcel.tracking_code, carrier_name=parcel.carrier_name, send_bcc=False)
                pp.pprint(tracked)
            except Exception as e:
                print(e)


    return JsonResponse({'message': 'Finished!'})

def submit_tracking(request):
    order_id = int(request.GET.get('order_id'))
    tracked_parcels = Parcel2GoShipment.objects.filter(
        p2g_order_id=order_id)

    etsy = EtsyClient()
    for parcel in tracked_parcels:
        try:
            tracked = etsy.submit_tracking(receipt_id=parcel.receipt_id.receipt_id,
                                    tracking_code=parcel.tracking_code, carrier_name=parcel.carrier_name, send_bcc=False)
            pp.pprint(tracked)
        except Exception as e:
            print(e)


    return JsonResponse({'message': 'Finished!'})
