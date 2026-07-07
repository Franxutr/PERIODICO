"""Orquestador del pipeline completo.

Uso:
  python main.py --dry-run   # ejecuta todo SIN publicar (recomendado al empezar)
  python main.py             # ejecuta y publica segun WP_DEFAULT_STATUS (draft/publish)

Programalo cada X minutos con cron o systemd para que funcione 24/7.
"""
import argparse
import ingest
import cluster
import write
import config

# Elige el publicador segun el destino configurado.
if config.PUBLISH_TARGET == "wordpress":
    import publish_wp as publisher
else:
    import publish_files as publisher

def main(dry_run=False):
    print("=== Ciclo del periodico ===")
    ingest.run()                          # [1] leer fuentes
    approved = cluster.run()              # [2] muro de seguridad (2+ fuentes)
    if not approved:
        print("Nada que redactar en este ciclo.")
        return
    # Limita cuantas noticias se redactan por vuelta (respeta el nivel gratuito).
    if len(approved) > config.MAX_ARTICLES_PER_RUN:
        print(f"[main] {len(approved)} grupos; se redactan {config.MAX_ARTICLES_PER_RUN} en esta vuelta.")
        approved = approved[:config.MAX_ARTICLES_PER_RUN]
    published, retained = 0, 0
    for group in approved:                # [3] redactar + verificar
        try:
            article = write.write_article(group)
        except Exception as e:
            print(f"[write] error en cluster {group['cluster_id']}: {e}")
            continue
        if article["status"] == "APTO":
            publisher.publish(article, dry_run=dry_run)   # [4] publicar (files o wordpress)
            published += 1
            # [5] redes: activar cuando este configurado
            # social.distribute(article, post_url)
        else:
            retained += 1
    print(f"=== Fin: {published} aptos, {retained} retenidos para revision ===")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no publica, solo simula")
    args = ap.parse_args()
    main(dry_run=args.dry_run)
