import os
from dotenv import load_dotenv

load_dotenv()

# Fabric Authentication
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ABFS_PATH = os.getenv("ABFS_PATH")

# Azure AI Search
SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")

# External API
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
FX_BASE_CURRENCY = os.getenv("FX_BASE_CURRENCY", "USD")
FX_API_BASE_URL = os.getenv("FX_API_BASE_URL")