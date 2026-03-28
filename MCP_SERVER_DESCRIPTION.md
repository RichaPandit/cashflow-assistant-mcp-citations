# Cashflow Agent MCP Server

## Overview

The **Cashflow Agent** is a Model Context Protocol (MCP) server that provides intelligent cashflow forecasting and financial document search capabilities. It integrates multiple enterprise data sources to deliver comprehensive financial insights with currency conversion and supporting documentation.

## Server Information

- **Name**: CashflowAgent
- **Protocol**: Model Context Protocol (MCP)
- **Transport**: Streamable HTTP
- **Endpoint**: `/mcp`
- **Authentication**: Bearer token via `x-agent-key` header

## Capabilities

### Tools

#### 1. `get_cashflow_forecast`
Retrieves cashflow forecast data from Microsoft Fabric Lakehouse with automatic currency conversion and supporting documentation.

**Parameters:**
- `query` (string): Search query for retrieving supporting documents from Azure AI Search

**Returns:** JSON object containing:
- `answer`: Natural language forecast summary
- `forecast_gbp`: Projected cashflow in GBP
- `forecast_usd`: Projected cashflow in USD (converted)
- `fx_rate`: Current GBP/USD exchange rate
- `citations`: Array of data sources with titles, URLs, and sources

**Use Case:** Get comprehensive cashflow projections with multi-currency support and automatic citation of data sources including Fabric data, exchange rates, and relevant financial documents.

---

#### 2. `search_documents_tool`
Searches SharePoint documents indexed in Azure AI Search for financial documentation and supporting materials.

**Parameters:**
- `query` (string): Search query text
- `top` (integer, optional): Maximum number of results to return (default: 3)

**Returns:** JSON array of document results with metadata including:
- `metadata_storage_name`: Document filename
- `content`: Extracted text content
- `metadata_storage_path`: Azure Blob Storage path

**Use Case:** Retrieve relevant financial documents, forecasts, reports, and policies from the organization's SharePoint document library.

---

#### 3. `get_exchange_rate`
Retrieves current exchange rates between two currencies using ExchangeRate-API.

**Parameters:**
- `base_currency` (string, optional): Base currency code (default: GBP)
- `target_currency` (string, optional): Target currency code (default: USD)

**Returns:** JSON object containing:
- `base`: Base currency code
- `target`: Target currency code
- `rate`: Current exchange rate

**Use Case:** Convert amounts between currencies or retrieve current exchange rates for financial analysis.

---

### Resources

#### `data://cashflow/fabric`
**Name:** FabricCashflow  
**Description:** Cashflow data from Microsoft Fabric Lakehouse  
**MIME Type:** application/json  
**Returns:** Array of raw cashflow values from the Fabric Lakehouse

**Use Case:** Direct access to underlying cashflow data for custom analysis or visualization.

---

## Technical Architecture

### Data Sources

1. **Microsoft Fabric Lakehouse**
   - Connection: ABFS (Azure Blob File System)
   - Purpose: Source of truth for cashflow forecast data
   - Format: Parquet files

2. **Azure Blob Storage**
   - Container: `cashflowsharepointdocs/cashflow-forecast`
   - Purpose: Document storage synced from SharePoint via Logic Apps
   - Content: PDFs, Excel files, and other financial documents

3. **Azure AI Search (Cognitive Search)**
   - Purpose: Semantic search over financial documents
   - Features: Foundry embeddings for RAG (Retrieval-Augmented Generation)
   - Query fields: `metadata_storage_name`, `content`, `metadata_storage_path`

4. **ExchangeRate-API**
   - Version: v6
   - Base Currency: GBP
   - Purpose: Real-time currency conversion

### Technology Stack

- **Framework**: FastMCP (Model Context Protocol implementation)
- **Runtime**: Python 3.11
- **Web Server**: Uvicorn (ASGI)
- **Authentication**: Custom Bearer token middleware
- **Dependencies**: fastmcp, fastapi, pandas, pyodbc, requests, PyPDF2

### Authentication

The server implements custom Bearer token authentication via the `UserAuthMiddleware`:

- **Header Name**: `x-agent-key` (or `api-key`)
- **Format**: `Bearer <token>`
- **Environment Variable**: `LOCAL_TOKEN` or `MCP_DEV_ASSUME_KEY`
- **Validation**: Exact string match against configured token

**Example Header:**
```
x-agent-key: Bearer cashflow-agent-secret-2026
```

### Deployment

**Azure App Service Configuration:**
- Platform: Linux
- Python Version: 3.11
- Startup Command: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
- Environment Variables: Configured via Application Settings
  - `LOCAL_TOKEN`: Authentication token
  - `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`: Azure AD credentials
  - `ABFS_PATH`: Fabric Lakehouse path
  - `SEARCH_ENDPOINT`, `SEARCH_KEY`: Azure AI Search credentials
  - `EXCHANGE_API_KEY`: ExchangeRate-API key
  - `FX_BASE_CURRENCY`: Base currency (GBP)

---

## Integration

### Copilot Studio Configuration

**MCP Connector Settings:**
1. **URL**: `https://<your-app-name>.azurewebsites.net/mcp`
2. **Authentication Type**: Custom Header
3. **Header Configuration**:
   - Name: `x-agent-key`
   - Value: `Bearer <your-token>`

### Use Cases

1. **Financial Planning**: Query cashflow forecasts with automatic currency conversion
2. **Document Discovery**: Search financial policies, reports, and forecasts
3. **Multi-Source Analysis**: Combine Fabric data, market rates, and documents
4. **Conversational Finance**: Natural language queries via Copilot Studio
5. **Cross-Currency Reporting**: Automatic GBP/USD conversion for international teams

---

## Error Handling

- **Authentication Errors**: Returns `ToolError` with descriptive messages
- **Missing Configuration**: Validates environment variables on startup
- **API Failures**: Graceful degradation with informative error messages
- **Search Failures**: Returns empty arrays rather than crashing

---

## Monitoring & Logging

- Standard output logging via Python `logging` module
- Azure App Service diagnostic logs
- Request/response tracking through Uvicorn logs
- Authentication attempt logging

---

## Data Flow

```
User Query (Copilot Studio)
    ↓
MCP Endpoint (/mcp)
    ↓
Bearer Token Authentication
    ↓
Tool Invocation
    ↓
┌─────────────────────────────────┐
│ get_cashflow_forecast           │
│  1. Query Fabric (ABFS)         │
│  2. Get FX Rate (API)           │
│  3. Search Documents (AI Search)│
│  4. Build Response + Citations  │
└─────────────────────────────────┘
    ↓
JSON Response with Citations
    ↓
Copilot Studio Display
```

---

## Version Information

- **MCP Protocol**: Latest
- **FastMCP**: Latest (with stateless HTTP support)
- **Python**: 3.11
- **Last Updated**: March 2026

---

## Support & Maintenance

**Configuration Files:**
- `config.py`: Environment variable loading
- `fabric.py`: Fabric Lakehouse connection
- `rag.py`: Azure AI Search queries
- `external_api.py`: Exchange rate API integration
- `requirements.txt`: Python dependencies

**Key Environment Variables Required:**
- `LOCAL_TOKEN`: Authentication token
- `SEARCH_ENDPOINT`: Azure AI Search endpoint
- `SEARCH_KEY`: Azure AI Search admin key
- `ABFS_PATH`: Fabric Lakehouse ABFS path
- `EXCHANGE_API_KEY`: ExchangeRate-API key

---

## Security Considerations

1. **Token Management**: Store tokens in Azure Key Vault or Application Settings (never in code)
2. **HTTPS Only**: Always use HTTPS for production deployments
3. **Credential Rotation**: Regularly rotate API keys and tokens
4. **Access Control**: Limit token distribution to authorized users/systems
5. **Audit Logging**: Enable Azure App Service diagnostic logs for audit trails

---

## Future Enhancements

- [ ] Multi-currency support beyond GBP/USD
- [ ] Historical forecast trends
- [ ] Document upload capabilities
- [ ] Real-time Fabric data sync
- [ ] Advanced search filters (date range, document type)
- [ ] Caching layer for frequently accessed data
