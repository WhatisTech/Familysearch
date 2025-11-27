import click, pathlib, json
from shared.crawler import yield_links, download
from shared.htr_router import route
from shared.name_extractor import extract
from shared.indexer import index

@click.command()
@click.argument("start_url")
@click.option("--limit", default=3, help="max files")
def run(start_url, limit):
    dest = pathlib.Path("data/download")
    for url, kind in yield_links(start_url):
        file = download(url, dest / (hashlib.md5(url.encode()).hexdigest() + f".{kind}"))
        text = route(file)
        persons = extract(text)
        if persons:
            index(persons)
            print("indexed", len(persons), "from", url)
        limit -= 1
        if not limit: break

if __name__ == "__main__":
    import hashlib
    run()