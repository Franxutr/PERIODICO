"""Valida que cada feed responde y trae entradas. Ejecutar antes de activar el motor."""
import yaml
import feedparser
import config

def run():
    with open(config.FEEDS_FILE, encoding="utf-8") as f:
        feeds = yaml.safe_load(f)["feeds"]
    print(f"Comprobando {len(feeds)} fuentes...\n")
    ok, ko = 0, 0
    for feed in feeds:
        url = feed.get("url", "")
        if url.startswith("API:") or not url:
            print(f"  [API] {feed['name']}: requiere modulo de API dedicado")
            continue
        try:
            parsed = feedparser.parse(url)
            n = len(parsed.entries)
            if n > 0:
                print(f"  [OK]  {feed['name']}: {n} entradas")
                ok += 1
            else:
                print(f"  [--]  {feed['name']}: responde pero 0 entradas (revisar URL)")
                ko += 1
        except Exception as e:
            print(f"  [ERR] {feed['name']}: {e}")
            ko += 1
    print(f"\nResultado: {ok} feeds validos, {ko} a revisar.")

if __name__ == "__main__":
    run()
