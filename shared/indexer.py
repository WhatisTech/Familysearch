import typesense, json, os

TS_HOST = os.getenv("TS_URI", "http://localhost:8108")
TS_KEY  = os.getenv("TS_KEY", "changeMe")

CLIENT = typesense.Client({
    "nodes": [{"host": TS_HOST.split("//")[-1], "port": "8108", "protocol": "http"}],
    "api_key": TS_KEY,
    "connection_timeout_seconds": 10
})

COLLECTION_NAME = "people"

def create_collection():
    schema = {
        "name": COLLECTION_NAME,
        "fields": [
            {"name": "surname", "type": "string", "locale": "pl"},
            {"name": "given", "type": "string[]", "locale": "pl"},
            {"name": "year", "type": "int32"},
            {"name": "raw", "type": "string"},
            {"name": "page_url", "type": "string"},
            {"name": "confidence", "type": "float"}
        ]
    }
    try:
        CLIENT.collections.create(schema)
    except typesense.exceptions.ObjectAlreadyExists:
        pass

def index(persons: list):
    create_collection()
    for p in persons:
        p["id"] = str(hash(p["raw"]) % 10**10)
    return CLIENT.collections[COLLECTION_NAME].documents.import_(persons)