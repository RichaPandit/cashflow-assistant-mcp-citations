import requests
from config import SEARCH_ENDPOINT, SEARCH_KEY

def search_documents(query, top=2):
    url = f"{SEARCH_ENDPOINT}/indexes/cashflow-index/docs/search?api-version=2023-11-01"
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