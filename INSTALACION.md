# INSTALACIÓN — todo desde cero, sin asumir nada

Este archivo se lee UNA vez por computador (y cuando algo falle). El uso
diario está en README.md.

# ============================================================
# PARTE 0 — QUÉ ES CADA COSA (en cristiano)
# ============================================================

- GIT / GITHUB / PUSH / PULL / LLAVE SSH: igual que en mis otros proyectos
  (si hace falta repasarlo, está en `plantilla-profesor/INSTALACION.md`).
- CLAUDE CODE: el programa `claude`; acá hace de entrenador.
- ENGRAM: la memoria del profe entre sesiones (MCP). Project = `Ajedrez`.
- UV: el gestor de Python que ya uso. Crea el entorno `.venv/` y corre el
  programa del repo con `uv run ajedrez ...`.
- STOCKFISH: el motor de ajedrez (el mismo que usan chess.com y lichess).
  Es el que verifica cada jugada que enseña el profe.
- PYTHON-CHESS: la biblioteca que lee las partidas y habla con Stockfish.
- API DE CHESS.COM: la puerta pública (solo lectura) por donde el programa
  baja mis partidas. No usa contraseña: mis partidas ya son públicas.

# ============================================================
# PARTE 1 — INSTALAR LO NECESARIO (una vez por PC)
# ============================================================

1. git, Claude Code y Engram: como en mis otros proyectos
   (`git --version`, `claude --version`, `engram --version`).
2. uv: `uv --version` (en Arch: `sudo pacman -S uv` si no está).
3. **Stockfish** (está en el AUR, no en los repos oficiales; compila unos
   minutos y pide la contraseña):
   ```
   yay -S stockfish
   ```
   Verificación: `stockfish <<< quit` → tiene que imprimir "Stockfish 19..."
4. **El entorno del repo** (dentro de la carpeta):
   ```
   cd ~/Proyectos/Ajedrez
   uv sync
   ```
5. **Verificación completa** (si esto da todo verde, está listo):
   ```
   uv run pytest -q
   uv run ajedrez partidas --ultimas 3
   ```
   `pytest` corre los tests (los del motor se saltean solos si Stockfish no
   está); `partidas` prueba la conexión con chess.com.

# ============================================================
# PARTE 2 — LLAVE SSH (una vez por PC)
# ============================================================

Igual que siempre: `ssh -T git@github.com` tiene que responder
"Hi Ander0296!". Si no, ver `plantilla-profesor/INSTALACION.md`, parte 2.

# ============================================================
# PARTE 3 — SUBIR ESTE REPO A GITHUB (una sola vez)
# ============================================================

El repo ya existe en mi PC (con su primer commit). Falta crearlo en GitHub.
**Lo decido yo**: el profe no crea repos por su cuenta.

¿Privado o público? Público funciona igual (el libro nunca sube: `material/`
está en `.gitignore`), pero el repo tiene mi usuario de chess.com y mis
partidas. Si dudo: privado.

Opción A — con `gh` (ya lo tengo instalado):
```
cd ~/Proyectos/Ajedrez
gh repo create Ander0296/Ajedrez --private --source . --remote origin --push
```
(cambiar `--private` por `--public` si lo quiero público)

Opción B — desde la web: github.com → "+" → New repository → nombre
`Ajedrez`, SIN README ni .gitignore → Create. Después:
```
cd ~/Proyectos/Ajedrez
git remote add origin git@github.com:Ander0296/Ajedrez.git
git push -u origin main
```

Desde ese momento, `/cierre` hace el push solo y el hook trae los cambios
al abrir cada sesión.

# ============================================================
# PARTE 4 — ENLAZAR UN SEGUNDO PC
# ============================================================

1. PARTE 1 y PARTE 2 en ese PC (incluido `yay -S stockfish`).
2. Clonar y preparar:
   ```
   cd ~/Proyectos
   git clone git@github.com:Ander0296/Ajedrez.git
   cd Ajedrez
   mkdir -p material/visto
   uv sync
   uv run pytest -q
   ```
   (`material/` y `datos/` llegan vacías A PROPÓSITO: no viajan por git. La
   caché de partidas se vuelve a bajar sola.)
3. La regla de oro con varios PCs la ejecuta el profe: `git pull` al
   empezar (`/arranque` y el hook), commit + push al terminar (`/cierre`).
4. Engram es LOCAL de cada PC: los archivos del repo son la fuente de verdad.

# ============================================================
# PARTE 5 — PROBLEMAS TÍPICOS
# ============================================================

- **"No encuentro Stockfish"**: falta `yay -S stockfish`, o está en otra
  ruta → ponerla en `ajedrez.toml` → `[motor] ruta = "/ruta/a/stockfish"`.
- **"chess.com respondió 429"**: demasiados pedidos seguidos. El programa
  reintenta solo; si persiste, esperar un minuto. Nunca correr dos comandos
  de partidas en paralelo.
- **"Sin conexión con chess.com"**: sin internet o chess.com caído. Lo ya
  bajado sigue en `datos/cache/` y `posicion` funciona sin red.
- **Una partida recién jugada no aparece**: la API de chess.com tarda unos
  minutos en publicarla. Probar de nuevo en 5-10 minutos.
- **`uv sync` falla por la versión de Python**: pegar el error en el chat;
  se resuelve fijando una versión (`uv python pin 3.13`).
- **Git pide usuario y contraseña al hacer push**: el repo quedó por HTTPS.
  `git remote set-url origin git@github.com:Ander0296/Ajedrez.git`.
- **Subí por error algo de `material/`**: avisarle al profe ANTES de hacer
  push; si ya se hizo push, hay que limpiar el historial (copyright).
