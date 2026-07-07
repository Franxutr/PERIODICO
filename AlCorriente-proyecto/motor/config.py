"""Configuracion central del motor. Lee variables de entorno desde .env."""
import os
from dotenv import load_dotenv

load_dotenv()

# IA
AI_PROVIDER = os.getenv("AI_PROVIDER", "anthropic")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-5")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Destino de publicacion: "files" (web en codigo / estatica) o "wordpress"
PUBLISH_TARGET = os.getenv("PUBLISH_TARGET", "files")

# WordPress
WP_URL = os.getenv("WP_URL", "").rstrip("/")
WP_USER = os.getenv("WP_USER", "")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")
WP_DEFAULT_STATUS = os.getenv("WP_DEFAULT_STATUS", "draft")

# Reglas de seguridad (el "muro")
MIN_SOURCES = int(os.getenv("MIN_SOURCES", "2"))
CLUSTER_SIMILARITY = float(os.getenv("CLUSTER_SIMILARITY", "0.62"))

# Fuentes de maxima autoridad: si aparece SOLO una de estas para su tema, se admite.
AUTHORITATIVE = {
    "BOE": ["Legislacion", "Nombramientos"],
    "AEMET": ["Tiempo", "Emergencias"],
    "INE": ["Datos"],
    "DGT": ["Trafico"],
    "IGN": ["Sismos"],
    "CGPJ": ["Justicia"],
}

DB_PATH = os.getenv("DB_PATH", "periodico.db")
FEEDS_FILE = os.getenv("FEEDS_FILE", "feeds.yaml")
