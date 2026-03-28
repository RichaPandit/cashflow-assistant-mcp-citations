import pandas as pd
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET, ABFS_PATH


def query_fabric_cashflow():

    storage_options = {
    "account_name": "onelake",
    "tenant_id": TENANT_ID,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
    }

    try:
        df = pd.read_parquet(ABFS_PATH, storage_options=storage_options)

        if "net_cashflow" in df.columns:
            raise Exception(f"Column 'net_cashflow' not found. Available: {df.columns}")
        values = df["net_cashflow"].dropna().tail(3).tolist()
        return values
    
    except Exception as e:
        print("Error reading Fabric via ABFS:", str(e))
        return []
