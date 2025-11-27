import click, pathlib, json
from shared.crawler import yield_links, download
from shared.htr_router import route
from shared.name_extractor import extract
from shared.indexer import index

@click.command()
@click.option("--demo", is_flag=True, help="index dummy data")
def demo(demo):
    if demo:
        dummy = [
            {"given": ["Jan"], "surname": "Novák", "year": 1903,
             "raw": "Novák, Jan 1903 teacher Veľký Krtíš", "page_url": "#", "confidence": 0.94},
            {"given": ["Anna"], "surname": "Novák", "year": 1900,
             "raw": "Novák, Anna 1900", "page_url": "#", "confidence": 0.91}
        ]
        from shared.indexer import index
        index(dummy)
        print("indexed demo")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo(True)