import os
import pprint

from django.utils.timezone import make_aware
from dotenv import load_dotenv
from etsy2 import Etsy
from etsy2.oauth import EtsyOAuthClient, EtsyOAuthHelper

from .models import CustomerDetail, EtsyOrder, OrderItem, Shipment

pp = pprint.PrettyPrinter(indent=4)


class EtsyClient():
    
    #permission_scopes = ["listings_r", "listings_w", "shops_rw"]
    load_dotenv()  # take environment variables from .env
    
    ETSY_API_KEY = os.environ.get('ETSY_API_KEY')
    ETSY_API_SECRET = os.environ.get('ETSY_API_SECRET')
    ETSY_OAUTH_TOKEN = os.environ.get('ETSY_OAUTH_TOKEN')
    ETSY_OAUTH_TOKEN_SECRET = os.environ.get('ETSY_OAUTH_TOKEN_SECRET')
    ETSY_SHOP_ID = os.environ.get('ETSY_SHOP_ID')
    
    def __init__(self):

        etsy_oauth = EtsyOAuthClient(
            client_key=self.ETSY_API_KEY,
            client_secret=self.ETSY_API_SECRET,
            resource_owner_key=self.ETSY_OAUTH_TOKEN,
            resource_owner_secret=self.ETSY_OAUTH_TOKEN_SECRET,
        )
        self.etsy_api = Etsy(etsy_oauth_client=etsy_oauth)

    def get_transactions(self, limit=25, offset=0):
        shop_id = self.ETSY_SHOP_ID
        return self.etsy_api.findAllShopTransactions(shop_id=shop_id, limit=limit, offset=offset)
    
    def process_orders(self, limit=25, offset=0):
        transactions = self.get_transactions(limit=limit, offset=offset)
        
        for transaction in transactions:
            order = EtsyOrder.add_order(transaction)
            receipt = self.process_receipt(transaction['receipt_id'], order)
            self.process_x(transaction['receipt_id'], order)
        
        return transaction
    
    def process_receipt_transactions(self, receipt_id, order):
        receipts = self.etsy_api.findAllShop_Receipt2Transactions(receipt_id=receipt_id)
        for receipt in receipts:
            OrderItem.add_order_item(receipt, order)
    
    def process_shop_receipts(self, limit=25, offset=0):
        receipts = self.etsy_api.findAllShopReceipts(shop_id=self.ETSY_SHOP_ID, limit=limit, offset=offset)
        for receipt in receipts:
            order = EtsyOrder.add_order(receipt)
            customer_detail = CustomerDetail.add_customer_detail(receipt, order)
            transactions = self.process_receipt_transactions(receipt['receipt_id'], order)
            if receipt['was_shipped']:
                for shipment in receipt['shipments']:
                    shipping_info = Shipment.add_shipping_detail(shipment, order)
