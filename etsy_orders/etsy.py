import os
from etsy2 import Etsy
from etsy2.oauth import EtsyOAuthClient, EtsyOAuthHelper
from dotenv import load_dotenv


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