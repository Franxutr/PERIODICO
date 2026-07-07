"""[4] Publicacion en WordPress via REST API.

Requiere un usuario con 'Application Password' (Ajustes > Usuarios en WordPress).
Publica en estado 'draft' por defecto: la publicacion real es una decision explicita.
"""
import requests
import config
import db

def _auth():
    return (config.WP_USER, config.WP_APP_PASSWORD)

def _footer(sources):
    links = " · ".join(f'<a href="{s["url"]}" rel="nofollow">{s["name"]}</a>' for s in sources)
    return (
        '<hr><p><em>Noticia elaborada automaticamente a partir de fuentes oficiales y '
        f'verificada por nuestro sistema. Fuentes: {links}.</em></p>'
    )

def get_or_create_category(name):
    r = requests.get(f"{config.WP_URL}/wp-json/wp/v2/categories",
                     params={"search": name}, auth=_auth())
    r.raise_for_status()
    for cat in r.json():
        if cat["name"].lower() == name.lower():
            return cat["id"]
    r = requests.post(f"{config.WP_URL}/wp-json/wp/v2/categories",
                      json={"name": name}, auth=_auth())
    r.raise_for_status()
    return r.json()["id"]

def publish(article, dry_run=False):
    content = f"<p><strong>{article['lead']}</strong></p>\n{article['body']}\n{_footer(article['sources'])}"
    payload = {
        "title": article["headline"],
        "content": content,
        "status": config.WP_DEFAULT_STATUS,   # draft | publish
        "categories": [get_or_create_category(article["section"])],
    }
    if dry_run:
        print(f"[wp][dry-run] '{article['headline']}' -> {payload['status']} en {article['section']}")
        return None
    r = requests.post(f"{config.WP_URL}/wp-json/wp/v2/posts", json=payload, auth=_auth())
    r.raise_for_status()
    post = r.json()
    db.mark_published(article["id"], post["id"])
    print(f"[wp] publicado id={post['id']} status={post['status']}")
    return post
