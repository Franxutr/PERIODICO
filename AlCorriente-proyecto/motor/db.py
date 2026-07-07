"""Modelo de datos minimo con SQLite. Guarda entradas crudas y articulos."""
import sqlite3
import json
from datetime import datetime
import config

def conn():
    c = sqlite3.connect(config.DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, topic TEXT, authority INTEGER,
            title TEXT, summary TEXT, link TEXT UNIQUE,
            published TEXT, fetched_at TEXT, cluster_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cluster_id INTEGER,
            headline TEXT, lead TEXT, body TEXT, section TEXT,
            sources_json TEXT,
            status TEXT,            -- APTO | RETENIDO | PUBLICADO | RECHAZADO
            verified INTEGER,
            wp_post_id INTEGER,
            created_at TEXT
        );
        """)

def add_entry(e):
    with conn() as c:
        try:
            c.execute(
                "INSERT OR IGNORE INTO entries (source,topic,authority,title,summary,link,published,fetched_at) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (e["source"], e["topic"], int(e["authority"]), e["title"],
                 e["summary"], e["link"], e["published"], datetime.utcnow().isoformat()),
            )
        except sqlite3.IntegrityError:
            pass

def unclustered_entries():
    with conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM entries WHERE cluster_id IS NULL")]

def set_cluster(entry_id, cluster_id):
    with conn() as c:
        c.execute("UPDATE entries SET cluster_id=? WHERE id=?", (cluster_id, entry_id))

def save_article(a):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO articles (cluster_id,headline,lead,body,section,sources_json,status,verified,created_at) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (a["cluster_id"], a["headline"], a["lead"], a["body"], a["section"],
             json.dumps(a["sources"], ensure_ascii=False), a["status"],
             int(a["verified"]), datetime.utcnow().isoformat()),
        )
        return cur.lastrowid

def mark_published(article_id, wp_post_id):
    with conn() as c:
        c.execute("UPDATE articles SET status='PUBLICADO', wp_post_id=? WHERE id=?",
                  (wp_post_id, article_id))
