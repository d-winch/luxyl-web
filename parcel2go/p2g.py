import os
import re
import requests
from .parcel import Parcel
from .address import Address
from typing import List
from os.path import join, dirname
from dotenv import load_dotenv


class P2G():

    BASE_URL = "https://www.parcel2go.com"

    AUTH_ENDPOINTS = {
        "auth": "/auth/connect/token",
        "oauth": "/auth/connect/authorize"
    }

    AUTH_HEADERS = {
        "Host": "www.parcel2go.com",
        "User-Agent": "insomnia/5.14.6",
        "Content-Type": "application/json",
        "Authorization": "",
        "Accept": "*/*"
    }

    def __init__(self):

        self.ENV_FILE = ".env"

        dotenv_path = join(dirname(__file__), self.ENV_FILE)
        load_dotenv(dotenv_path)

        self.SANDBOX = False
        self.BASE_URL = os.environ.get("BASE_URL")
        self.HOST = os.environ.get("HOST")
        self.CLIENT_ID = os.environ.get("CLIENT_ID")
        self.CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
        self.ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
        self.AUTH_HEADERS["Authorization"] = f"Bearer {self.ACCESS_TOKEN}"

    def get_new_token(self):
        data = {
            "grant_type": "client_credentials",
            "scope": "public-api payment",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }

        headers = {
            "Host": self.HOST,
            "User-Agent": "insomnia/5.14.6",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*"
        }

        URL = f"{self.BASE_URL}{self.AUTH_ENDPOINTS['auth']}"
        r = requests.post(URL, headers=headers, data=data)
        self.ACCESS_TOKEN = r.json().get('access_token')
        self.AUTH_HEADERS["Authorization"] = f"Bearer {self.ACCESS_TOKEN}"
        self.write_env_file()

    def write_env_file(self):
        with open(join(dirname(__file__), self.ENV_FILE), 'r') as env_file:
            data = env_file.read()
        with open(join(dirname(__file__), self.ENV_FILE), 'w') as env_file:
            data = re.sub(r"\nACCESS_TOKEN=.*\n",
                          f"\nACCESS_TOKEN={self.ACCESS_TOKEN}\n", data)
            env_file.write(data)

    def requires_access_token(func):
        def wrapper(self, *args, **kwargs):
            req = func(self, *args, **kwargs)
            if req.status_code == 401:
                print(f"Token expired, obtaining new token...")
                self.get_new_token()
                req = func(self, *args, **kwargs)
            return req
        return wrapper

    @requires_access_token
    def get_orders(self):
        return requests.get(f"{self.BASE_URL}/api/me/orders/detail", headers=self.AUTH_HEADERS)

    @requires_access_token
    def get_quote(self, postcode: str, parcel: Parcel, service_slug: str = "inpost"):
        length, width, height = parcel.dimensions
        quote = {
            "Service": service_slug,
            "Upsells": [
                {"type": "ExtendedBaseCover"}
            ],
            "CollectionAddress": {
                "Country": "GBR",
                "Postcode": "TR8 4JP"
            },
            "DeliveryAddress": {
                "Country": "GBR",
                "Postcode": postcode
            },
            "Parcels": [
                {
                    "Value": parcel.total_parcel_cost,
                    "Weight": parcel.weight_kg,
                    "Length": length,
                    "Width": width,
                    "Height": height
                }
            ]
        }
        return requests.post(f"{self.BASE_URL}/api/quotes", headers=self.AUTH_HEADERS, json=quote)

    @requires_access_token
    def verify_order(self, addresses: List[Address], parcels: List[Parcel], collection_date: str, service_slug: str = "inpost"):

        shipments = []

        for parcel, address in zip(parcels, addresses):
            length, width, height = parcel.dimensions
            shipments.append(
                {
                    "Id": parcel.etsy_reference,
                    "CollectionDate": collection_date,
                    "Parcels": [
                        {
                            #"Id": "00000000-0000-0000-0000-000000000000",
                            "Length": length,
                            "Height": height,
                            "Width": width,
                            "EstimatedValue": parcel.total_parcel_cost,
                            "Weight": parcel.weight_kg,
                            "DeliveryAddress": {
                                "ContactName": address.contact_name,
                                "Email": address.email,
                                "Phone": address.phoneno,
                                "Property": address.property,
                                "Street": address.street,
                                "Town": address.town,
                                "County": address.county,
                                "Postcode": address.postcode,
                                "CountryIsoCode": address.country_iso_code,
                                "CountryId": address.country_id
                            },
                            "ContentsSummary": parcel.contents
                        }
                    ],
                    "Service": service_slug,
                    "Upsells": [
                        {"type": "ExtendedBaseCover"}
                    ],
                    "CollectionAddress": {
                        "ContactName": "Returns",
                        "Organisation": "Luxyl",
                        "Email": "accounts@luxyl.co",
                        "Phone": "07517248051",
                        "Property": "Horseshoe Barn",
                        "Street": "Rialton Barton",
                        "Locality": "",
                        "Town": "Newquay",
                        "County": "Cornwall",
                        "Postcode": "TR8 4JP",
                        "CountryIsoCode": "GBR",
                        "CountryId": 0,
                        "SpecialInstructions": ""
                    }
                }
            )

        order = {
            "Items": shipments,
            "CustomerDetails": {
                "Email": "d.winchy@gmail.com",
                "Forename": "David",
                "Surname": "Winch"
            }
        }
        return requests.post(f"{self.BASE_URL}/api/orders/verify", headers=self.AUTH_HEADERS, json=order)
    
    @requires_access_token
    def create_order(self, addresses: List[Address], parcels: List[Parcel], collection_date: str, service_slug: str = "inpost"):

        shipments = []

        for parcel, address in zip(parcels, addresses):
            length, width, height = parcel.dimensions
            shipments.append(
                {
                    "Id": parcel.etsy_reference,
                    "CollectionDate": collection_date,
                    "Parcels": [
                        {
                            "Id": parcel.etsy_reference,
                            "Length": length,
                            "Height": height,
                            "Width": width,
                            "EstimatedValue": parcel.total_parcel_cost,
                            "Weight": parcel.weight_kg,
                            "DeliveryAddress": {
                                "ContactName": address.contact_name,
                                "Email": address.email,
                                "Phone": "07517248051",
                                "Property": address.property,
                                "Street": address.street,
                                "Town": address.town,
                                "County": address.county,
                                "Postcode": address.postcode,
                                "CountryIsoCode": address.country_iso_code,
                                "CountryId": address.country_id
                            },
                            "ContentsSummary": parcel.contents
                        }
                    ],
                    "Service": service_slug,
                    "CollectionAddress": {
                        "ContactName": "Returns",
                        "Organisation": "Luxyl",
                        "Email": "accounts@luxyl.co",
                        "Phone": "07517248051",
                        "Property": " ",
                        "Street": "Horseshoe Barn, Rialton Barton",
                        "Locality": "",
                        "Town": "Newquay",
                        "County": "Cornwall",
                        "Postcode": "TR8 4JP",
                        "CountryIsoCode": "GBR",
                        "CountryId": 0,
                        "SpecialInstructions": ""
                    }
                }
            )

        order = {
            "Items": shipments,
            "CustomerDetails": {
                "Email": "d.winchy@gmail.com",
                "Forename": "David",
                "Surname": "Winch"
            }
        }
        return requests.post(f"{self.BASE_URL}/api/orders", headers=self.AUTH_HEADERS, json=order)

    @requires_access_token
    def purchase_order_with_prepay(self, order_id: str):
        return requests.post(f"{self.BASE_URL}/api/orders/{order_id}/paywithprepay", headers=self.AUTH_HEADERS)

    @requires_access_token
    def get_tracking_codes_and_parcel_ids(self, order_id: str):
        return requests.post(f"{self.BASE_URL}/api/orders/{order_id}/parcelnumbers", headers=self.AUTH_HEADERS)
    
    @requires_access_token
    def get_tracking_codes_from_line_id(self, line_id: str):
        return requests.get(f"{self.BASE_URL}/api/tracking/{line_id}", headers=self.AUTH_HEADERS)

    @requires_access_token
    def get_labels(self, order_id: str, detail: str = "Labels", media: str = "Label4x6", label_format: str = "PDF"):

        # $detail = $detail == 'label' ? 'Labels' : 'All';
        # $media = $media == 'thermal' ? 'Label4x6' : 'A4';

        params = {
            "referenceType": "OrderId",
            "detailLevel": detail,
            "labelMedia": media,
            "labelFormat": label_format
        }
        return requests.get(f"{self.BASE_URL}/api/labels/{order_id}/separate", headers=self.AUTH_HEADERS, params=params)

    @requires_access_token
    def get_prepay_balance(self):
        return requests.get(f"{self.BASE_URL}/api/prepay", headers=self.AUTH_HEADERS)

    @requires_access_token
    def get_prepay_topup_link(self, amount: int = 100):
        data = {
            "Amount": amount,
            "CurrencyCode": "GBP"
        }
        return requests.post(f"{self.BASE_URL}/api/prepay/create-topup-links", headers=self.AUTH_HEADERS, json=data)


class P2GSandbox(P2G):

    AUTH_HEADERS = {
        "Host": "sandbox.parcel2go.com",
        "User-Agent": "insomnia/5.14.6",
        "Content-Type": "application/json",
        "Authorization": "",
        "Accept": "*/*"
    }

    def __init__(self):

        self.ENV_FILE = ".env_sandbox"
        dotenv_path = join(dirname(__file__), self.ENV_FILE)
        load_dotenv(dotenv_path)

        self.SANDBOX = True
        self.BASE_URL = os.environ.get("BASE_URL")
        self.HOST = os.environ.get("HOST")
        self.CLIENT_ID = os.environ.get('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
        self.ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
        self.AUTH_HEADERS["Authorization"] = f"Bearer {self.ACCESS_TOKEN}"
