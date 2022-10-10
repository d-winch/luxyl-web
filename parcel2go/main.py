import pprint
import webbrowser
#from requests.models import to_native_string
from datetime import datetime, timedelta

import p2g
from address import Address
from parcel import Item, Parcel

pp = pprint.PrettyPrinter(indent=4)

p2g = p2g.P2GSandbox()

# TODO: Create items programmatically
item = Item(name="T-Shirt", unit_price=14.99, weight_kg=0.15,
            length=30, width=23, height=3, qty=1)
item2 = Item(name="Hoodie", unit_price=22.99, weight_kg=0.6,
             length=30, width=23, height=7, qty=1)
item3 = Item(name="Zipped Hoodie", unit_price=23.99,
             weight_kg=0.65, length=30, width=23, height=7, qty=2)

# TODO: Add etsy reference
# TODO: Add address into parcel object
parcel = Parcel([item, item2, item3], etsy_reference="0123456789")

# TODO: Add address
address = Address(
    contact_name="David Winch",
    email="d.winchy@gmail.com",
    phone="07517248051",
    property="",
    street="69 Pendragon Crescent",
    town="Newquay",
    county="Cornwall",
    postcode="TR2 3EQ"
)
address2 = Address(
    contact_name="David Winch",
    email="d.winchy@gmail.com",
    phone="07517248051",
    property="69",
    street="Pendragon Crescent",
    town="Newquay",
    county="Cornwall",
    postcode="TR3 2BA"
)
address3 = Address(
    contact_name="David Winch",
    email="d.winchy@gmail.com",
    phone="07517248051",
    property="69",
    street="Pendragon Crescent",
    town="Newquay",
    county="Cornwall",
    postcode="TR4 2WS"
)

quotes = p2g.get_quote(postcode=address.postcode,
                       parcel=parcel, service_slug="inpost").json()

print("\n###### Quote ######")
pp.pprint(quotes)

# if quotes["Quotes"]:
#     print(quotes["Quotes"][0].get("TotalPrice"))
#     collection_date = datetime.fromisoformat(
#         quotes["Quotes"][0].get("Collection"))
#     if datetime.now().hour > 12:
#         collection_date = collection_date + timedelta(days=1, hours=12)
#     collection_date = collection_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
#     print(collection_date)

collection_date = datetime.utcnow().replace(
    hour=0, minute=0, second=0, microsecond=0)
if datetime.now().hour > 12:
    collection_date = collection_date + timedelta(days=1, hours=12)
collection_date = collection_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")


addresses = [address, address2, address3]
parcels = [parcel, parcel, parcel]

order_verification = p2g.verify_order(
    addresses=addresses,
    parcels=parcels,
    collection_date=collection_date,
    service_slug="inpost"
)

print("\n###### Order Verification ######")
pp.pprint(order_verification.json())

order = p2g.create_order(
    addresses=addresses,
    parcels=parcels,
    collection_date=collection_date,
    service_slug="inpost"
)

print("\n###### Order ######")
pp.pprint(order.json())

order_id = order.json()["OrderId"]
ordered_parcels = {}
for order_line in order.json()["OrderlineIdMap"]:
    
    ordered_parcels[order_line["OrderLineId"]] = {
        "item_id": order_line["ItemId"],
        "hash": order_line["Hash"]
    }

print("\n", "###### Price and Balance ######")
print("Order total:", order.json()['TotalPrice'])
print("Prepay Balance:", p2g.get_prepay_balance().json())

print("\n", "###### Payment Link ######")
print(order.json()['Links']['payment'])
webbrowser.open_new_tab(order.json()['Links']['payment'])


# payment = p2g.purchase_order_with_prepay(order_id=order_id)
# print("\n###### Payment ######")
# pp.pprint(payment.json())
# labels_6x4 = payment.json()['Links'][2]['Link']
# print("Label link:", labels_6x4)

input("Please pay for the order using the above link and then hit enter to continue...")

# tracking = p2g.get_tracking_codes_and_parcel_ids(order_id=order_id)
# pp.pprint(tracking.json())
# print(f"Order ID: {order_id}")

print("\n###### Ordered Parcel Details ######")

labels = p2g.get_labels(order_id=order_id)

for label in labels.json()["Items"]:
    order_line_id = label["OrderLineId"]
    tracking_no = label["CourierTrackingNumbers"][0]
    ordered_parcels[str(order_line_id)]["tracking_no"] = tracking_no

pp.pprint(ordered_parcels)

# TODO: send tracking and reference to etsy api
for order_line, vals in ordered_parcels.items():
    print(order_line)
    print(vals["item_id"], vals["tracking_no"])
exit(0)
# label_base64 = str.encode(labels.json()["Items"][0]["Base64EncodedLabel"])

# for label in labels.json()["Items"]:
#     label_order = label["OrderLineId"]
#     label_data = str.encode(label["Base64EncodedLabel"])
#     with open(f"{label_order}.pdf", "wb") as f:
#         f.write(codecs.decode(label_data, "base64"))

# with open("test.pdf", "wb") as f:
#     f.write(codecs.decode(label_base64, "base64"))

# p = p2g.get_prepay_topup_link(amount=120)
