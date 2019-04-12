# This example uses Python 2.7+ and the python-request library
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests



class JsonData:

    def __init__(self):
        pass

    def get_latest_bitcoin_price(self, session, crypto_api_url, crypto_parameters):
        try:
            response = session.get(crypto_api_url, params=crypto_parameters)
            data = json.loads(response.text)['data']
            # for item in data:
            #     print(item)
            return float(data[0]['quote']['USD']['price'])
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    def post_ifttt_webhook(self, event, value, ifttt_webhooks_url):
        # The payload that will be sent to IFTTT service
        data = {'value1': value}
        # Inserts desired event
        ifttt_event_url = ifttt_webhooks_url.format(event)
        # Sends a HTPP POST request to the webhook URL
        requests.post(ifttt_event_url, json=data)

