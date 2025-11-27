import os, typesense, json
from shared.indexer import COLLECTION_NAME

TS_CLIENT = typesense.Client({
    "nodes": [{"host": os.getenv("TS_URI", "localhost").split("://")[-1], "port": "8108", "protocol": "http"}],
    "api_key": os.getenv("TS_KEY", "changeMe"),
    "connection_timeout_seconds": 2
})

def search(given: str, surname: str, year: int = None, more: dict = None, limit=3):
    q = f"{given} {surname}".strip()
    filter_by = []
    if year:
        filter_by.append(f"year: [{year-2}..{year+2}]")
    if more:
        if more.get("village"):
            filter_by.append(f"village:={more['village']}")
    search_parameters = {
        "q": q,
        "query_by": "given,surname",
        "filter_by": " && ".join(filter_by) if filter_by else "",
        "per_page": limit,
        "sort_by": "_text_match:desc,year:asc"
    }
    res = TS_CLIENT.collections[COLLECTION_NAME].documents.search(search_parameters)
    hits = []
    for h in res.get("hits", []):
        d = h["document"]
        hits.append({
            "id": d["id"],
            "name": f"{d['given'][0]} {d['surname']}",
            "year": d.get("year"),
            "snippet": d["raw"][:120] + "…",
            "score": h["text_match"]
        })
    return {"found": res["found"], "hits": hits}