import os
from dotenv import load_dotenv

load_dotenv()

# Fabric
ABFS_PATH = os.getenv("ABFS_PATH")

# Azure AI Search
SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")

# External API
FX_API = "https://api.exchangerate.host/latest?base=GBP"