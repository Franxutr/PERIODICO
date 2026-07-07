# Motor de automatización — [NOMBRE DEL PERIÓDICO]

Scaffold en Python de la "redacción robotizada": ingesta de fuentes oficiales → agrupación y corroboración (muro de seguridad) → redacción original con IA → verificación anti-alucinación → publicación en WordPress → difusión en redes.

> Este es un esqueleto funcional y comentado, pensado para que tú o un desarrollador lo pongáis en marcha. No publica nada solo hasta que configures las credenciales y actives cada paso. Empieza siempre en modo BORRADOR.

## Estructura

```
motor/
├── config.py          # Configuración central y variables de entorno
├── feeds.yaml         # Lista de fuentes (se alimenta del CSV de fuentes)
├── feed_checker.py    # Valida que cada feed/URL responde antes de usarlo
├── ingest.py          # [1] Lee RSS/APIs y guarda entradas en la base de datos
├── cluster.py         # [2] Agrupa por hecho y aplica la regla de 2+ fuentes
├── write.py           # [3] Redacta el artículo de cero + verifica con IA
├── publish_wp.py      # [4] Publica en WordPress vía REST API
├── social.py          # [5] Prepara y envía piezas a redes (stubs)
├── db.py              # Modelo de datos (SQLite por defecto)
├── main.py            # Orquestador: encadena todo el pipeline
└── requirements.txt
```

## Puesta en marcha (resumen)

1. `pip install -r requirements.txt`
2. Copia `.env.example` a `.env` y rellena claves (OpenAI/Anthropic, WordPress, redes).
3. `python feed_checker.py` — comprueba qué fuentes responden.
4. `python main.py --dry-run` — ejecuta todo SIN publicar (deja borradores).
5. Cuando estés conforme, programa `python main.py` cada X minutos (cron / systemd).

## Filosofía de seguridad

- Nada se publica si no hay **≥2 fuentes** coincidentes (o 1 de máxima autoridad).
- Todo artículo pasa un **verificador** que comprueba que cada frase se apoya en las fuentes.
- Lo dudoso queda en estado `RETENIDO` para revisión humana.
- Modo `--dry-run` y estado `borrador` por defecto: la publicación real es una decisión explícita.
