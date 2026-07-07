"""[1] Ingesta: lee los feeds oficiales y guarda entradas nuevas en la BD."""
import yaml
import feedparser
import db
import config

def load_feeds():
    with open(config.FEEDS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)["feeds"]

def run():
    db.init()
    feeds = load_feeds()
    total = 0
    for feed in feeds:
        url = feed.get("url", "")
        if not url or url.startswith("API:"):
            # Las fuentes por API (AEMET, INE JSON, IGN...) se implementan en modulos aparte.
            continue
        parsed = feedparser.parse(url)
        for item in parsed.entries:
            db.add_entry({
                "source": feed["name"],
                "topic": feed.get("topic", ""),
                "authority": feed.get("authority", False),
                "title": getattr(item, "title", "").strip(),
                "summary": getattr(item, "summary", "").strip(),
                "link": getattr(item, "link", "").strip(),
                "published": getattr(item, "published", ""),
            })
            total += 1
    print(f"[ingest] procesadas {total} entradas de {len(feeds)} fuentes")

if __name__ == "__main__":
    run()
