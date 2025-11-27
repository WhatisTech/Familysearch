import streamlit as st
import os, uuid, json, datetime, sqlite3
from shared.search import search
from shared.cli import index_sample   # helper for demo

st.set_page_config(page_title="Family HTR Search", layout="wide")
st.title("🔍 Family Search – Eastern-European Handwriting")

@st.cache_resource
def init_history():
    conn = sqlite3.connect("search_history.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS history(
        id TEXT PRIMARY KEY, ts TEXT, query TEXT, top3 TEXT, starred INTEGER)""")
    conn.commit()
    return conn

conn = init_history()

def save_search(query, top3):
    conn.execute("INSERT INTO history(id,ts,query,top3,starred) VALUES (?,?,?,?,?)",
                 (str(uuid.uuid4()), datetime.datetime.utcnow().isoformat(),
                  json.dumps(query), json.dumps(top3), 0))
    conn.commit()

def person_card(hit):
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://dummyimage.com/120x160/ddd/000.jpg&text=page", width=100)
        with col2:
            st.markdown(f"**{hit['name']}**  ‑  {hit['year']}")
            st.caption(hit["snippet"])
            st.progress(hit["score"] / 100)
        return st.button("Explore family", key=f"exp_{hit['id']}")

tab1, tab2 = st.tabs(["Search", "History"])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1: given = st.text_input("Given name")
    with c2: surname = st.text_input("Surname")
    with c3: year = st.number_input("Year", min_value=1700, max_value=2100, step=1, value=1900)
    if st.button("Search"):
        if not surname:
            st.error("Surname is required")
            st.stop()
        res = search(given, surname, year)
        save_search({"given": given, "surname": surname, "year": year}, res["hits"])
        st.success(f"{res['found']} hits")
        for h in res["hits"][:3]:
            person_card(h)

with tab2:
    st.subheader("Search History")
    rows = conn.execute("SELECT id, ts, query, starred FROM history ORDER BY ts DESC LIMIT 50").fetchall()
    for rid, ts, q, star in rows:
        q = json.loads(q)
        st.text(f"{ts}  –  {q['given']} {q['surname']}  {q['year']}")