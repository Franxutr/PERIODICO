"""[2] Agrupacion + corroboracion: el 'muro de seguridad'.

Agrupa entradas que hablan del mismo hecho por similitud semantica y decide si un
grupo puede avanzar: necesita >= MIN_SOURCES fuentes distintas, o 1 fuente de
maxima autoridad para su tema.
"""
import db
import config
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None

def model():
    global _model
    if _model is None:
        # Modelo multilingue ligero; funciona bien en espanol.
        _model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _model

def run():
    entries = db.unclustered_entries()
    if not entries:
        print("[cluster] no hay entradas nuevas")
        return []

    texts = [f"{e['title']} {e['summary']}" for e in entries]
    emb = model().encode(texts, normalize_embeddings=True)
    sim = cosine_similarity(emb)

    # Agrupacion greedy por umbral de similitud.
    clusters, assigned = [], set()
    for i in range(len(entries)):
        if i in assigned:
            continue
        group = [i]
        assigned.add(i)
        for j in range(i + 1, len(entries)):
            if j not in assigned and sim[i][j] >= config.CLUSTER_SIMILARITY:
                group.append(j)
                assigned.add(j)
        clusters.append(group)

    approved = []
    for cid, group in enumerate(clusters, start=1):
        members = [entries[k] for k in group]
        for m in members:
            db.set_cluster(m["id"], cid)
        sources = {m["source"] for m in members}
        has_authority = any(m["authority"] for m in members)
        if len(sources) >= config.MIN_SOURCES or has_authority:
            approved.append({"cluster_id": cid, "members": members,
                             "reason": "authority" if has_authority else f"{len(sources)} fuentes"})
        # else: queda registrado pero no aprobado -> revision humana

    print(f"[cluster] {len(clusters)} grupos, {len(approved)} superan el muro de seguridad")
    return approved

if __name__ == "__main__":
    run()
