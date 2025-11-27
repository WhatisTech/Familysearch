import re, json, pathlib

# basic Polish / East-EU diacritic folding
FOLD = str.maketrans("ąćęłńóśźżčďěľľňřšťýž", "acelnoszzcdellnrs ty z")

# common given-name variants
SYN = {
    "jan": ["jan", "janos", "ivan", "johann", "john"],
    "stanislaw": ["stanislaw", "staszek", "stanek"],
    "anna": ["anna", "ania", "hanna"],
}

def normalize(word: str) -> str:
    return word.lower().translate(FOLD)

def extract(text: str):
    lines = text.splitlines()
    people = []
    for line in lines:
        # naive regex: word , word year
        m = re.search(r'(\w+),\s*(\w+).*\b(\d{4})\b', line)
        if m:
            surname, given, year = normalize(m.group(1)), normalize(m.group(2)), int(m.group(3))
            given_vars = SYN.get(given, [given])
            people.append({"surname": surname, "given": given_vars, "year": year, "raw": line.strip()})
    return people