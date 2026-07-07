# Cómo tener las noticias automáticas 24/7 (sin tu ordenador encendido)

## La idea, en claro

Tu ordenador **no** tiene que estar encendido. El programa que rastrea las fuentes y redacta las noticias se ejecuta **en la nube** —en un ordenador que ya está encendido siempre y que no es tuyo—, disparado por un reloj automático. Aunque cierres el portátil, apagues la luz y te vayas de vacaciones, sigue funcionando.

La forma más simple y **gratuita** de conseguirlo, y que encaja con una web "hecha en código", es **GitHub Actions**: subes el código a GitHub y GitHub lo ejecuta cada 20 minutos en sus propios servidores. Ya te dejo el archivo que hace eso.

## Cómo funciona el circuito

```
Reloj de GitHub (cada 20 min)
        │
   Arranca el motor en un servidor de GitHub
        │
   Lee fuentes oficiales → verifica 2+ → redacta de cero
        │
   Guarda cada noticia como archivo (Markdown + feed.json)
        │
   GitHub hace 'commit' de las noticias nuevas
        │
   Tu web se redespliega sola y las muestra
```

Nada de esto pasa por tu ordenador. Todo vive en la nube.

## Por qué "sin copyright"

El motor **no copia** de las fuentes: toma el hecho, lo **reescribe con sus propias palabras** y enlaza el origen oficial. Además, solo publica lo confirmado por dos o más fuentes. Por eso es legal y no plagia.

## Qué te he dejado preparado

- **`.github/workflows/noticias.yml`** — el archivo que automatiza todo. Ejecuta el motor cada 20 minutos, sin tu ordenador. Puedes cambiar la frecuencia (la línea `cron: "*/20 * * * *"`).
- **`motor/publish_files.py`** — hace que el motor guarde cada noticia como un archivo Markdown (con su título, entradilla, fuentes y sello de IA) y mantenga un `feed.json` con las últimas 100. Así tu web las lee sin necesidad de base de datos.
- El motor ya sabe elegir entre **guardar archivos** (`PUBLISH_TARGET=files`, lo que usaremos) o publicar en WordPress, según prefieras.

## Puesta en marcha (pasos)

1. **Sube el proyecto a GitHub.** Crea un repositorio (privado está bien) y sube la carpeta `motor/`, la carpeta `.github/` y tu web. La estructura queda así:
   ```
   tu-repo/
   ├── .github/workflows/noticias.yml
   ├── motor/            (el motor en Python)
   ├── content/          (aquí caerán las noticias: se crea sola)
   └── (los archivos de tu web)
   ```

2. **Guarda tu clave de IA como "secreto".** En GitHub: *Settings → Secrets and variables → Actions → New repository secret*. Nómbralo `ANTHROPIC_API_KEY` y pega tu clave. Nunca va en el código; queda cifrada. *(Esto solo lo puedes hacer tú: la clave va con tu cuenta y tu tarjeta.)*

3. **Completa las fuentes.** En `motor/feeds.yaml`, pon las URLs reales de los feeds oficiales (las tienes en `fuentes-nacionales.csv`). Ejecuta antes `feed_checker.py` para ver cuáles responden.

4. **Prueba sin publicar.** En la pestaña *Actions* de GitHub, pulsa "Run workflow" a mano y revisa que genera noticias correctas en `content/noticias/`.

5. **Déjalo corriendo.** A partir de ahí se ejecuta solo cada 20 minutos, para siempre. Revisa de vez en cuando la carpeta de retenidos y los resultados.

## Cuando decidas el hosting de la web

Este montaje funciona con casi cualquier web en código (Next.js, Astro, Hugo, etc.), porque las noticias son simples archivos que tu web lee. Cuando elijas dónde alojarla:

- Si va en **Vercel / Netlify / Cloudflare Pages**: cada vez que GitHub guarda una noticia, tu web se **redespliega sola**. No hay que tocar nada más.
- Si prefieres una **base de datos** (Supabase, Postgres) en vez de archivos, se cambia el publicador y listo; dímelo y te lo preparo.

## Notas útiles

- **Coste:** GitHub Actions es gratis para uso normal (tienes minutos de sobra al mes). Solo pagarías la IA (tu clave) según el volumen de noticias.
- **Frecuencia:** cada 20 min está bien para empezar. Puedes bajar a 10 o subir a 30 según cuántas noticias quieras y el gasto de IA.
- **Fiabilidad:** si un ciclo falla (una fuente caída), el siguiente lo retoma. GitHub te avisa por correo si algo peta.
- **Alternativa siempre-encendida:** si algún día quieres algo aún más continuo, un VPS pequeño (~5 €/mes) con `cron` hace lo mismo. Pero para arrancar, GitHub Actions te sobra.
