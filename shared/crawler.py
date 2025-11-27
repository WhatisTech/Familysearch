import requests, re, os, json, hashlib
from urllib.parse import urljoin
from pathlib import Path

USER_AGENT = "FamilyHTR-Crawler/1.0"

def yield_links(entry_url: str):
    """Breadth-first harvest of PDF/JPG/JP2."""
    visited, queue = set(), [entry_url]
    while queue:
        url = queue.pop(0)
        if url in visited: continue
        visited.add(url)
        try:
            r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        except Exception as e:
            print("SKIP", url, e); continue
        ct = r.headers.get("content-type", "")
        if "pdf" in ct or url.lower().endswith(".pdf"):
            yield url, "pdf"
        elif "image" in ct or url.lower().endswith((".jpg", ".jpeg", ".jp2")):
            yield url, "image"
        # parse HTML for more links
        for href in re.findall(r'href=["\']([^"\']+\.(?:pdf|jpe?g|jp2))', r.text, re.I):
            queue.append(urljoin(url, href))

def download(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists(): return dest
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    return dest