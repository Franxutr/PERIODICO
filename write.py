"""[3] Redaccion + verificacion con IA.

Redacta el articulo DE CERO a partir solo de los hechos de las fuentes oficiales.
Luego un segundo paso verifica que cada afirmacion se apoya en esas fuentes.
"""
import json
import config
import db

REDACTION_PROMPT = """Eres redactor de un periodico digital riguroso. A partir UNICAMENTE de los
siguientes hechos procedentes de fuentes oficiales, redacta una noticia ORIGINAL en espanol.

REGLAS ESTRICTAS:
- No copies frases literales de las fuentes; reescribe todo con tus palabras.
- No anadas ningun dato que no este en las fuentes. Si algo no consta, no lo inventes.
- Tono informativo, neutral y claro. Estructura: titular, entradilla y cuerpo.
- No opines. No especules. Atribuye los datos a su fuente cuando proceda.

FUENTES:
{sources}

Devuelve SOLO un JSON valido con las claves: headline, lead, body, section.
La seccion debe ser una de: Nacional, Politica, Economia, Sociedad, Sucesos, Tribunales,
Salud, Ciencia, Cultura, Deportes, Tiempo, Internacional.
"""

VERIFY_PROMPT = """Eres verificador de datos. Comprueba si CADA afirmacion del ARTICULO esta
respaldada por las FUENTES. Si hay alguna afirmacion no respaldada, inventada o exagerada,
responde con "verified": false y explica cual.

FUENTES:
{sources}

ARTICULO:
{article}

Devuelve SOLO un JSON: {{"verified": true/false, "issues": ["..."]}}
"""

import time
_last_call = [0.0]

def _throttle():
    """Espera lo justo entre llamadas para respetar el limite gratuito."""
    wait = config.AI_MIN_INTERVAL - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.time()

def _call_ai(prompt):
    """Llama al proveedor configurado. Devuelve texto."""
    _throttle()
    if config.AI_PROVIDER == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        msg = client.messages.create(
            model=config.AI_MODEL, max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    else:
        # Groq, Gemini y OpenAI comparten la API de OpenAI: solo cambia la URL base.
        from openai import OpenAI
        client = OpenAI(api_key=config.AI_API_KEY, base_url=config.AI_BASE_URL)
        r = client.chat.completions.create(
            model=config.AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return r.choices[0].message.content

def _json(text):
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1])

def write_article(cluster):
    members = cluster["members"]
    sources_txt = "\n\n".join(
        f"- Fuente: {m['source']} ({m['topic']})\n  Titular: {m['title']}\n  Resumen: {m['summary']}\n  URL: {m['link']}"
        for m in members
    )
    draft = _json(_call_ai(REDACTION_PROMPT.format(sources=sources_txt)))
    check = _json(_call_ai(VERIFY_PROMPT.format(
        sources=sources_txt,
        article=json.dumps(draft, ensure_ascii=False))))

    verified = bool(check.get("verified"))
    article = {
        "cluster_id": cluster["cluster_id"],
        "headline": draft["headline"],
        "lead": draft["lead"],
        "body": draft["body"],
        "section": draft.get("section", "Nacional"),
        "sources": [{"name": m["source"], "url": m["link"]} for m in members],
        "verified": verified,
        "status": "APTO" if verified else "RETENIDO",
    }
    article_id = db.save_article(article)
    article["id"] = article_id
    if not verified:
        print(f"[write] articulo {article_id} RETENIDO: {check.get('issues')}")
    return article
