"""[4-bis] Publicacion como ARCHIVOS (para webs 'en codigo' / sitios estaticos).

Escribe cada noticia como un Markdown con front-matter en content/noticias/ y
mantiene un feed.json con las ultimas. Asi tu web (en cualquier framework) lee esos
archivos y los muestra. No necesita base de datos.

En GitHub Actions, tras ejecutarse, el workflow hace commit de estos archivos y tu
web se redespliega sola. Cero ordenador encendido.
"""
import os
import re
import json
from datetime import datetime, timezone
import config
import db

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "content/noticias")
FEED_PATH = os.getenv("FEED_PATH", "content/feed.json")


def _slug(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")[:80]


def _sources_md(sources):
    return " · ".join(f"[{s['name']}]({s['url']})" for s in sources)


def publish(article, dry_run=False):
    now = datetime.now(timezone.utc)
    slug = f"{now:%Y-%m-%d}-{_slug(article['headline'])}"
    fname = os.path.join(OUTPUT_DIR, f"{slug}.md")

    front = {
        "title": article["headline"],
        "lead": article["lead"],
        "section": article["section"],
        "date": now.isoformat(),
        "sources": article["sources"],
        "ai_generated": True,
        "verified": bool(article.get("verified", True)),
    }
    body = (
        "---\n"
        + json.dumps(front, ensure_ascii=False, indent=2)
        + "\n---\n\n"
        + f"**{article['lead']}**\n\n"
        + article["body"]
        + "\n\n---\n"
        + f"*Noticia elaborada automaticamente a partir de fuentes oficiales y verificada. "
        + f"Fuentes: {_sources_md(article['sources'])}.*\n"
    )

    if dry_run:
        print(f"[files][dry-run] {fname}")
        return None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(body)

    _update_feed(article, slug, now)
    db.mark_published(article["id"], 0)
    print(f"[files] escrito {fname}")
    return fname


def _update_feed(article, slug, now, limit=100):
    items = []
    if os.path.exists(FEED_PATH):
        try:
            items = json.load(open(FEED_PATH, encoding="utf-8"))
        except Exception:
            items = []
    items.insert(0, {
        "slug": slug,
        "title": article["headline"],
        "lead": article["lead"],
        "section": article["section"],
        "date": now.isoformat(),
        "sources": article["sources"],
    })
    items = items[:limit]
    os.makedirs(os.path.dirname(FEED_PATH), exist_ok=True)
    json.dump(items, open(FEED_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
