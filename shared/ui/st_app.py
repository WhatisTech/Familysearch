import streamlit as st
import os, uuid, json, datetime
import requests
import sqlite3

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

tab1, tab2 = st.tabs(["Search", "History"])

with tab1:
    given = st.text_input("Given name")
    surname = st.text_input("Surname")
    year  = st.number_input("Year", min_value=1700, max_value=2100, step=1, value=1900)
    if st.button("Search"):
        query = {"given": given, "surname": surname, "year": year}
        top3  = [{"name": f"{given} {surname}", "year": year, "id": "dummy1"}]  # stub
        st.success(f"Top-3 hits for {given} {surname}")
        for hit in top3:
            st.write("•", hit["name"], hit["year"])
        save_search(query, top3)

with tab2:
    st.subheader("Search History")
    rows = conn.execute("SELECT id, ts, query, starred FROM history ORDER BY ts DESC").fetchall()
    for rid, ts, q, star in rows:
        q = json.loads(q)
        st.text(f"{ts}  –  {q['given']} {q['surname']}  {q['year']}")