
from datetime import datetime
import time
from app import JsonData
from requests import  Session

BITCOIN_LOW_PRICE_THRESHOLD = 5000
BITCOIN_HIGH_PRICE_THRESHOLD = 6000

CRYPTO_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
CRYPTO_PARAMETERS = {
    'start': '1',
    'limit': '10',
    'convert': 'USD'
}
CRYPTO_HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '{key}', # you should provide actual key here
}

session = Session()
session.headers.update(CRYPTO_HEADERS)
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{key}' # you should provide actual key here

def main():
    bitcoin_history = []
    while True:
        price = JsonData().get_latest_bitcoin_price(session, CRYPTO_API_URL, CRYPTO_PARAMETERS)
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_LOW_PRICE_THRESHOLD:
            JsonData().post_ifttt_webhook('bitcoin_price_emergency', price, IFTTT_WEBHOOKS_URL)
            print('wyslano')

        if price > BITCOIN_HIGH_PRICE_THRESHOLD:
            JsonData().post_ifttt_webhook('bitcoin_price_emergency', price, IFTTT_WEBHOOKS_URL)
        # Send an email notification
        # Once we have 5 items in our bitcoin history send an update
        print(bitcoin_history)
        if len(bitcoin_history) == 5:
            JsonData().post_ifttt_webhook('bitcoin_price_update', _format_bitcoin_history(bitcoin_history),
                                          IFTTT_WEBHOOKS_URL)

            # Reset the history
            bitcoin_history = []

        # Sleep for 5 minute/1 hour - 5 minute is just for testing purposes
        # time.sleep(1 * 60)
        time.sleep(5 * 3600)


def _format_bitcoin_history(bitcoin_history):
    rows = []
    print(bitcoin_history[0])
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        # price = bitcoin_price.get('price', 0)
        print(bitcoin_price.get('date'))
        price = bitcoin_price['price']
        print(price)
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)

if __name__ == '__main__':
    main()
