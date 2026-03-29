import logging
import pandas as pd
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET, ABFS_PATH

logger = logging.getLogger(__name__)


def query_fabric_cashflow():

    storage_options = {
        "account_name": "onelake",
        "tenant_id": TENANT_ID,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        logger.info("Reading parquet from ABFS path: %s", ABFS_PATH)
        df = pd.read_parquet(ABFS_PATH, storage_options=storage_options)
        logger.info("Parquet loaded. Shape: %s, Columns: %s", df.shape, df.columns.tolist())

        if "net_cashflow" not in df.columns:
            logger.error("Column 'net_cashflow' not found. Available: %s", df.columns.tolist())
            return []

        values = df["net_cashflow"].dropna().tail(3).tolist()
        logger.info("Cashflow values: %s", values)
        return values

    except Exception as e:
        logger.error("Error reading Fabric via ABFS: %s", str(e), exc_info=True)
        return []
