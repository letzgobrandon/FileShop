import json
import requests
from django.shortcuts import get_object_or_404
from .models import Product
from django.conf import settings


base_url = "https://www.blockonomics.co/api"
headers = {"Authorization": "Bearer " + settings.BLOCKONOMICS_API_KEY}
conversion = {"BTC": lambda currency: f"{base_url}/price?currency={currency}"}

class BlockonomicsAPIError(Exception):
    pass

def exchanged_rate(amount, crypto, currency) -> float:
    url = conversion[crypto](currency)
    r = requests.get(url)
    response = r.json()
    return round(pow(10, 8) * amount / response["price"])

def exchanged_rate_to_usd(amount, crypto, currency) -> float:
    url = conversion[crypto](currency)
    r = requests.get(url)
    response = r.json()
    return round (amount * response["price"], 2)


def create_order(product, crypto):
    url = f"{base_url}/new_address"
    response = requests.post(url, headers=headers)
    if response.status_code not in range(200, 299):
        if response.status_code in range(400, 499):
            response.raise_for_status()
        
        try:
            data = response.json()
            error = "[%s] %s (Status %s)" % (data.get('error_code', 'UNKNOWN_CODE'), data.get('message', "No Error Message"), data.get('status', response.status_code))
            raise BlockonomicsAPIError(error)
        except json.JSONDecodeError:
            raise BlockonomicsAPIError(response.content)
    address = response.json()["address"]
    price = exchanged_rate(product.price, crypto, product.currency)/pow(10, 8)

    return address, price
