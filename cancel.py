import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import orders

ACCESS_TOKEN = ''
SECRET_KEY = ''
URL = 'https://api.coinone.co.kr/v2/order/cancel/'

PAYLOAD = {
  "access_token": ACCESS_TOKEN,
  "order_id": "OrderID",
  "price": 500000,
  "qty": 0.1,
  "is_ask": 1,
  "currency": "qtum"
}

def get_encoded_payload(payload):
  payload[u'nonce'] = int(time.time()*1000)

  dumped_json = json.dumps(payload)
  encoded_json = base64.b64encode(dumped_json)
  return encoded_json

def get_signature(encoded_payload, secret_key):
  signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
  return signature.hexdigest()

def get_response(url, payload):
  encoded_payload = get_encoded_payload(payload)
  headers = {
    'Content-type': 'application/json',
    'X-COINONE-PAYLOAD': encoded_payload,
    'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
  }
  http = httplib2.Http()
  response, content = http.request(URL, 'POST', headers=headers, body=encoded_payload)
  return content

def get_result():
  content = get_response(URL, PAYLOAD)
  content = json.loads(content)

  return content

if __name__   == "__main__":

    myOrder = orders.get_result()
    #print myOrder['limitOrders'][0]['orderId']

    PAYLOAD['order_id'] = myOrder['limitOrders'][0]['orderId']
    PAYLOAD['price'] = myOrder['limitOrders'][0]['price']
    PAYLOAD['qty'] = myOrder['limitOrders'][0]['qty']

    print PAYLOAD
    print get_result()
