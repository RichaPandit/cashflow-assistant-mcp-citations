# Cashflow Agent

## Overview

Cashflow Agent is an AI-powered service that provides cashflow forecasts, currency exchange rates, and document search capabilities by integrating with Microsoft Fabric Lakehouse, Azure AI Search, and external FX APIs. It is built using FastMCP and exposes tools and resources for use in Model Context Protocol (MCP) environments.

## Features

- **Cashflow Forecasting**: Retrieves and summarizes cashflow data from Microsoft Fabric Lakehouse, with optional monthly breakdown and FX conversion.
- **Document Search**: Searches SharePoint and other documents synces regaulary to Azure Storage Account Container via a LogicApps flow, indexed in Azure AI Search, returning relevant documents and citations.
- **Exchange Rate Lookup**: Fetches real-time currency exchange rates between GBP and USD (or other currencies).
- **Resource Exposure**: Exposes Fabric cashflow data as a resource for use in MCP workflows.
- **Authentication Middleware**: Supports API key-based authentication for secure access (can be disabled for testing).

## Endpoints & Tools

- `/mcp` (ASGI app): Main endpoint for MCP tool and resource access.
- **Tools**:
  - `get_cashflow_forecast(query: str)`: Returns a cashflow forecast, FX rate, and supporting documents for a given query.
  - `search_documents_tool(query: str, top: int = 3)`: Searches documents and returns top results.
  - `get_exchange_rate(base_currency: str = "GBP", target_currency: str = "USD")`: Returns the current exchange rate.
- **Resource**:
  - `data://cashflow/fabric`: Raw cashflow data from Fabric Lakehouse.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   - `MCP_DEV_ASSUME_KEY` or `LOCAL_TOKEN`: API key for authentication (required unless auth is disabled).
   - `HOST` (optional): Host to bind the server (default: `0.0.0.0`).
   - `PORT` (optional): Port to run the server (default: `8000`).

3. **Run the server**:
   ```bash
   python main.py
   ```

4. **Access the MCP endpoint**:
   - The server will be available at `http://<host>:<port>/mcp`.
   - Use the provided tools and resources via MCP-compatible clients or directly via HTTP.

## Configuration

- **Authentication**: By default, the server expects a Bearer token in the `x-agent-key` or `api-key` header. To disable authentication for testing, comment out the line adding `UserAuthMiddleware` in `main.py`.
- **External Integrations**:
  - **Fabric Lakehouse**: Ensure access and credentials are configured for data retrieval.
  - **Azure AI Search**: Configure connection for document search.
  - **FX API**: Set up access to the external exchange rate API.

## File Structure

- `main.py` — Main server and tool definitions
- `fabric.py` — Fabric Lakehouse integration
- `rag.py` — Azure AI Search integration
- `external_api.py` — FX rate API integration
- `config.py` — Configuration and constants
- `requirements.txt` — Python dependencies
- `README.md` — This documentation

## License

See project for license details.

## Contact

For questions or support, please contact the project maintainer.
