import requests
from config import FX_API

def get_fx_rate():
    res = requests.get(FX_API).json()
    return res['rates']['USD']