from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .models import EtsyOrder


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1SVwVTUxlslvACFM8o9s28Nq1zjhXltSWX8Ec8uf1g04'

def orders_to_sheets(orders):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./etsy_orders/google_credentials/token.json'):
        creds = Credentials.from_authorized_user_file('./etsy_orders/google_credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './etsy_orders/google_credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('etsy_orders/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    order_data = [["Receipt ID", "Name", "Address", "Is Express", "Message", "Paid", "Total", "Creation Date", "Complete"]]
    order_item_data = [["Transaction ID", "SKU", "Title", "Size", "Price", "Quantity", "Receipt ID"]]
    
    for order in orders:
        order_details = [
            str(order.receipt_id),
            order.customerdetail_set.all()[0].name,
            order.customerdetail_set.all()[0].formatted_address,
            str(order.is_express),
            order.message_from_buyer,
            str(order.was_paid),
            str(order.grandtotal),
            str(order.creation_tsz),
            "False"
        ]
        order_data.append(order_details)
        
        for item in order.orderitem_set.all():
            order_item = [
                str(item.transaction_id),
                str(item.sku),
                item.title,
                item.property_values_size,
                str(item.price),
                str(item.quantity),
                str(item.receipt_id)
            ]
            order_item_data.append(order_item)
    
    order_sheetId = 0
    order_item_sheetId = 358232026
    
    order_rows = [{'values': [{'userEnteredValue': {'stringValue': f}} for f in e]} for e in order_data]
    rng = {'sheetId': order_sheetId, 'startRowIndex': 0, 'startColumnIndex': 0}
    fields = 'userEnteredValue'
    body_clear = {"requests": [{"updateCells": {"range": {"sheetId": order_sheetId}, "fields": "userEnteredValue"}}]}
    order_body = {'requests': [{'updateCells': {'rows': order_rows, 'range': rng, 'fields': fields}}]}
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body_clear)
    response = request.execute()
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=order_body)
    response = request.execute()
    
    order_item_rows = [{'values': [{'userEnteredValue': {'stringValue': f}} for f in e]} for e in order_item_data]
    rng = {'sheetId': order_item_sheetId, 'startRowIndex': 0, 'startColumnIndex': 0}
    fields = 'userEnteredValue'
    body_clear = {"requests": [{"updateCells": {"range": {"sheetId": order_item_sheetId}, "fields": "userEnteredValue"}}]}
    order_item_body = {'requests': [{'updateCells': {'rows': order_item_rows, 'range': rng, 'fields': fields}}]}
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body_clear)
    response = request.execute()
    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=order_item_body)
    response = request.execute()
    

if __name__ == '__main__':
    orders_to_sheets()