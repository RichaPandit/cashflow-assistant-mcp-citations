import os
from dotenv import load_dotenv

load_dotenv()

# Fabric (ODBC)
FABRIC_CONN_STR = os.getenv("FABRIC_CONN_STR")
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ABFS_PATH = os.getenv("ABFS_PATH")

# Azure AI Search
SEACRH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")

# Sharepoint
GRAPH_TOKEN = os.getenv("GRAPH_TOKEN")
SITE_ID = os.getenv("SITE_ID")

# External API
FX_API = "https://api.exchangerate.host/latest?base=GBP"