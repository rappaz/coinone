import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time
import sys
import balance

ACCESS_TOKEN = ''
SECRET_KEY = ''
URL = 'https://api.coinone.co.kr/v2/order/limit_buy/'

PAYLOAD = {
  "access_token": ACCESS_TOKEN,
  "price": 10,
  "qty": 0.01,
  "currency": "btc"
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

	price = sys.argv[2]
	qty = sys.argv[3]
	myBalance = balance.get_result()

	PAYLOAD['currency'] = 'qtum'
	PAYLOAD['price'] = int(price)
	PAYLOAD['qty'] = float(qty)

	print (" ===================== LIMIT BUY ===================== ")
	print ("Available KRW : %s" % str(myBalance['krw']['avail']))

  	if ( input("if you wanna quit, press 1 : ") == 1 ) : 
		print "Quit"
		exit()
	else :
		print "SELL"
		#print get_result()
