"""[5] Difusion en redes (stubs listos para conectar APIs oficiales).

Activar por fases. Cada red exige credenciales y cuentas de tipo profesional/business.
Empieza por Facebook + Instagram (Meta Graph API) y X; TikTok en modo asistido.
"""
import requests
import config

def build_caption(article, url):
    return f"{article['headline']}\n\n{article['lead']}\n\nLee mas: {url}\n\n#Espana #Noticias"

# --- Meta (Facebook + Instagram) ---
def post_facebook(article, url):
    if not config.__dict__.get("META_ACCESS_TOKEN"):
        print("[social][facebook] sin credenciales, omitido")
        return
    # POST https://graph.facebook.com/{PAGE_ID}/feed  (message, link)
    # Documentacion: Meta Graph API - Page feed.
    print("[social][facebook] TODO: implementar con Meta Graph API")

def post_instagram(article, image_url):
    # Flujo IG: crear media container -> publicar. Requiere imagen (usa portada generada).
    print("[social][instagram] TODO: implementar con Meta Graph API (media container)")

# --- X (Twitter) ---
def post_x(article, url):
    # POST https://api.twitter.com/2/tweets con OAuth 1.0a/2.0
    print("[social][x] TODO: implementar con X API v2")

# --- TikTok (asistido) ---
def prepare_tiktok(article):
    # Generar guion + vertical (titular + imagen/voz) y dejarlo en cola para revision.
    print("[social][tiktok] guion preparado para revision manual")

def distribute(article, post_url, image_url=None):
    post_facebook(article, post_url)
    if image_url:
        post_instagram(article, image_url)
    post_x(article, post_url)
    prepare_tiktok(article)
