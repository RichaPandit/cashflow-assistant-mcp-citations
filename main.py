import os
import logging
import json
from typing import Dict, List, Any

from fabric import query_fabric_cashflow
from rag import search_documents
from external_api import get_fx_rate

# FastMCP
from fastmcp.server import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.http import create_streamable_http_app

try:
    from fastmcp.server.exceptions import ToolError
except Exception:
    class ToolError(Exception):
        pass

# -----------------
# Config & constants
# -----------------
HEADER_NAME = "x-agent-key"
LOCAL_TOKEN: str = os.getenv("MCP_DEV_ASSUME_KEY", os.getenv("LOCAL_TOKEN", "")).strip()

# -----------------
# Auth middleware
# -----------------
class UserAuthMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        headers = get_http_headers()

        mcp_api_key = headers.get(HEADER_NAME) or headers.get("api-key")
        if not mcp_api_key:
            raise ToolError("Access denied: no key provided")

        if not mcp_api_key.startswith("Bearer "):
            logging.info("invalid token format in %s", HEADER_NAME)
            raise ToolError("Access denied: invalid token format")

        token = mcp_api_key.removeprefix("Bearer ").strip()
        expected = (LOCAL_TOKEN or "").strip()
        if not expected:
            raise ToolError("Access denied: server not configured")
        if token != expected:
            raise ToolError("Access denied: invalid token")

        return await call_next(context)

# -----------------
# FastMCP app
# -----------------
mcp = FastMCP(
    name="CashflowAgent",
)
mcp.add_middleware(UserAuthMiddleware())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------
# TOOLS
# -----------------

@mcp.tool()
def get_cashflow_forecast(query: str) -> str:
    """
    Get cashflow forecast from Fabric Lakehouse with FX conversion and supporting documents.
    Returns JSON with forecast, FX rate, and citations from Azure AI Search.
    
    Args:
        query: Search query for supporting documents
    """
    # 1. Fabric via ABFS
    values = query_fabric_cashflow()

    if values:
        forecast = sum(values) / len(values)
    else:
        forecast = 0

    # 2. FX API
    fx_rate = get_fx_rate()

    # 3. Azure AI Search (Blob PDFs)
    docs_rag = search_documents(query)

    # 4. Build answer with citations
    answer = f"Projected cash flow is £{int(forecast)} (~${int(forecast * fx_rate)})."

    # 5. Citations
    citations = [
        {
            "title": "Fabric Lakehouse (ABFS)",
            "url": "https://app.fabric.microsoft.com/",
            "source": "Fabric"
        },
        {
            "title": "Exchange Rate API",
            "url": "https://api.exchangerate-api.com",
            "source": "API"
        }
    ]

    for d in docs_rag:
        citations.append({
            "title": d.get("metadata_storage_name", "Document"),
            "url": d.get("metadata_storage_path", ""),
            "source": d.get("source", "Azure AI Search")
        })

    # 6. Format Output
    result = {
        "answer": answer,
        "forecast_gbp": int(forecast),
        "forecast_usd": int(forecast * fx_rate),
        "fx_rate": fx_rate,
        "citations": citations
    }

    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def search_documents_tool(query: str, top: int = 3) -> str:
    """
    Search SharePoint documents indexed in Azure AI Search.
    
    Args:
        query: Search query
        top: Maximum number of results (default: 3)
    """
    docs = search_documents(query, top)
    return json.dumps(docs, ensure_ascii=False)

@mcp.tool()
def get_exchange_rate(base_currency: str = "GBP", target_currency: str = "USD") -> str:
    """
    Get current exchange rate between two currencies.
    
    Args:
        base_currency: Base currency code (default: GBP)
        target_currency: Target currency code (default: USD)
    """
    rate = get_fx_rate(base_currency, target_currency)
    result = {
        "base": base_currency,
        "target": target_currency,
        "rate": rate
    }
    return json.dumps(result, ensure_ascii=False)

# -----------------
# RESOURCES
# -----------------

@mcp.resource("data://cashflow/fabric", name="FabricCashflow",
              description="Cashflow data from Microsoft Fabric Lakehouse",
              mime_type="application/json")
def res_fabric_cashflow() -> List[float]:
    """Returns raw cashflow values from Fabric"""
    return query_fabric_cashflow()

# --------------------------
# ASGI app & direct run
# --------------------------
app = create_streamable_http_app(
    server=mcp,
    streamable_http_path="/mcp",
    json_response=True,
    stateless_http=True,
    debug=False,
)

@app.get("/")
def home():
    return {"status": "running"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    mcp.run(transport="streamable-http", host=host, port=port, path="/mcp")