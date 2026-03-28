import requests
from PyPDF2 import PdfReader
import io
from config import GRAPH_TOKEN, SITE_ID

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def list_pdf_files(site_id):
    url = f"{GRAPH_BASE}/sites/{site_id}/drive/root/children"
    headers = {
        "Authorization": f"Bearer {GRAPH_TOKEN}"
    }
    res = requests.get(url, headers=headers).json()
    pdfs = [{"id": f["id"], "name": f["name"], "url": f["webUrl"]}
            for f in res.get("value", []) if f["name"].endswith(".pdf")]
    return pdfs

def download_pdf(file_id):
    url = f"{GRAPH_BASE}/sites/{SITE_ID}/drive/items/{file_id}/content"
    headers = {
        "Authorization": f"Bearer {GRAPH_TOKEN}"
    }
    res = requests.get(url, headers=headers)
    return res.content

def extract_text_from_pdf(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text