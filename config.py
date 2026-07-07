"""Configuracion central del motor. Lee variables de entorno desde .env."""
import os
from dotenv import load_dotenv

load_dotenv()

# IA  ── proveedor: "groq" (GRATIS, sin tarjeta) | "anthropic" | "openai" | "gemini"
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
AI_MODEL = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
# Clave del proveedor elegido (para Groq: GROQ_API_KEY). Cae a las especificas si existen.
AI_API_KEY = (os.getenv("AI_API_KEY") or os.getenv("GROQ_API_KEY")
              or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY") or "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# URL base para proveedores compatibles con OpenAI (Groq, Gemini, etc.)
_BASE = {
    "groq": "https://api.groq.com/openai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "openai": None,
}
AI_BASE_URL = os.getenv("AI_BASE_URL") or _BASE.get(AI_PROVIDER)

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
