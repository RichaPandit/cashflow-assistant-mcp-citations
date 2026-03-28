import requests
from config import SEARCH_ENDPOINT, SEARCH_KEY

def search_documents(query, top=3):
    """
    Query Azure Cognitive Search for documents indexed from Azure Blob Storage.
    """

    url = f"{SEARCH_ENDPOINT}/indexes/rag-1774725409174/docs/search?api-version=2023-11-01"
    headers = {
        "api-key": SEARCH_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "search": query,
        "top": top,
        "select": "metadata_storage_name,content,metadata_storage_path"
    }
    res = requests.post(url, headers=headers, json=body)
    return res.json().get("value", [])