import requests
from sharepoint import list_pdf_files, download_pdf, extract_text_from_pdf
from config import SEACRH_ENDPOINT, SEARCH_KEY, SITE_ID, GRAPH_TOKEN
import json

DELTA_FILE = "delta_link.txt"

def load_delta_link():
    try:
        with open(DELTA_FILE, 'r') as f:
            return f.read().strip()
    except:
        return None
    
def save_delta_link(link):
    with open(DELTA_FILE, 'w') as f:
        f.write(link)

def get_changes():
    delta_link = load_delta_link()
    url = delta_link or f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drive/root/delta"
    headers = {
        "Authorization": f"Bearer {GRAPH_TOKEN}"
    }
    res = requests.get(url, headers=headers).json()
    return res

def push_to_search(docs):
    url = f"{SEACRH_ENDPOINT}/indexes/{SEARCH_KEY}/docs/index?api-version=2023-11-01"
    headers = { "api-key": SEARCH_KEY, "Content-Type": "application/json" }
    body = {"value": docs}
    requests.post(url, headers=headers, json=body)

def run_pipeline():
    data = get_changes()
    documents = []
    for item in data.get("value", []):
        if "file" not in item or not item['name'].endswith('.pdf'):
            continue
        pdf_bytes = download_pdf(SITE_ID, item['id'])
        text = extract_text_from_pdf(pdf_bytes)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        for i, chunk in enumerate(chunks):
            documents.append({
                "@search.action": "upload",
                "id": f"{item['id']}_{i}",
                "content": chunk,
                "title": item['name'],
                "url": item['webUrl'],
                "lastModified": item['lastModifiedDateTime']
            })
    if documents:
        push_to_search(documents)
    delta_link = data.get("@odata.deltaLink")
    if delta_link:
        save_delta_link(delta_link)

if __name__ == "__main__":
    run_pipeline()