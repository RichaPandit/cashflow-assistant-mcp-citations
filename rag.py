import logging
import requests
from config import SEARCH_ENDPOINT, SEARCH_KEY

logger = logging.getLogger(__name__)

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
    logger.info("Searching index at: %s | query: %s", url, query)
    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        logger.info("Search HTTP status: %s", res.status_code)
        if res.status_code != 200:
            logger.error("Search error response: %s", res.text)
            return []
        data = res.json()
        logger.info("Search returned %s results", len(data.get('value', [])))
        return data.get("value", [])
    except Exception as e:
        logger.error("Search request failed: %s", str(e), exc_info=True)
        return []