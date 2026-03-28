import requests
from config import SEARCH_ENPOINT, SEARCH_KEY

def search_documents(query, top=2):
    url = f"{SEARCH_ENPOINT}/indexes/cashflow-index/docs/search?api-version=2023-11-01"
    headers = {
        "api-key": SEARCH_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "search": query,
        "top": top,
        "select": "title,content,url,source"
    }

    res = requests.post(url, headers=headers, json=body)
    return res.json().get("value", [])