import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import balance
import sys

ACCESS_TOKEN = ''
SECRET_KEY = ''
URL = 'https://api.coinone.co.kr/v2/order/limit_sell/'

PAYLOAD = {
  "access_token": ACCESS_TOKEN,
  "price": 0,
  "qty": 0.0,
  "currency": ""
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

def get_result(payload):
  content = get_response(URL, payload)
  content = json.loads(content)

  return content

if __name__   == "__main__":

  price = sys.argv[2]
  myBalance = balance.get_result()

  payload = {
    "access_token": ACCESS_TOKEN,
    "price": int(price),
    "qty": float(myBalance['qtum']['avail']),
    "currency": 'qtum'
  }
    
  print (" ===================== LIMIT SELL ===================== ")
  print ("Available QTUM : %s" % str(myBalance['qtum']['avail']))
  print payload

  if ( input("if you wanna quit, press 1 : ") == 1 ) : 
    print "Quit"
    exit()

  else :
    print "SELL"
    print get_result(payload)
