from fastapi import FastAPI
from fabric import query_fabric_cashflow
from rag import search_documents
from external_api import get_fx_rate
from sharepoint import list_pdf_files, download_pdf, extract_text_from_pdf
from config import SITE_ID

app = FastAPI()

@app.get("/cashflow")
def cashflow_agent(query: str):
    # 1. Fabric via ABFS
    values = query_fabric_cashflow()

    if values:
        forecast = sum(values) / len(values)
    else:
        forecast = 0

    # 2. FX API
    fx_rate = get_fx_rate()

    # 3. RAG / SharePoint PDFs
    docs_rag = search_documents(query)
    pdfs = list_pdf_files(SITE_ID)
    docs_live = []

    for pdf in pdfs:
        try:
            pdf_bytes = download_pdf(SITE_ID, pdf["id"])
            text = extract_text_from_pdf(pdf_bytes)
            if query.lower() in text.lower():
                docs_live.append({
                    "title": pdf["name"],
                    "url": pdf["url"],#
                    "content": text[:500],
                    "source": "SharePoint (Live PDF)"
                })
        except:
            continue

    # 4. Combine docs and format answer
    docs = docs_rag + docs_live

    # 5. Build answer with citations
    answer = f"Projected cash flow is £{int(forecast)} (~${int(forecast * fx_rate)})."

    # 6. Citations
    citations = [
        {
            "title": "Fabric Lakehouse (ABFS)",
            "url": "https://app.fabric.microsoft.com/",
             "source": "Fabric"
        },
        {
            "title": "Exchange Rate API",
            "url": "https://api.exchangerate.host",
            "source": "API"
        }
    ]

    citations.extend([
        {
            "title": d["title"],
            "url": d["url"],
            "source": d.get("source", "RAG")
        }
        for d in docs
    ])

    # 7. Format Output
    sources = "\n".join([f"- {c['title']}: {c['url']}" for c in citations])
    final_answer = f"{answer}\n\nSources:\n{sources}"
    return {"answer": final_answer}

@app.get("/")
def home():
    return {"status": "running"}