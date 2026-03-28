import requests
from config import EXCHANGE_API_KEY as API_KEY, FX_BASE_CURRENCY as BASE_CURRENCY, FX_API_BASE_URL

def get_fx_rate(base_currency=None, target_currency="USD"):
    if base_currency is None:
        base_currency = BASE_CURRENCY
    url = f"{FX_API_BASE_URL}/{API_KEY}/latest/{base_currency}"
    res = requests.get(url).json()
    return res['conversion_rates'][target_currency]