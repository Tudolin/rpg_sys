# Deploying RPG Sys on a self-hosted Debian box

RPG Sys has no external service dependencies by default: the database is a
single SQLite file on disk (`local_db.py`), and sessions/Socket.IO work
fine with a single process. Redis is entirely optional — only add it if you
later want to run more than one worker process.

## 1. System packages

O backend é Flask + Socket.IO; o frontend é uma SPA em Vue 3 + TypeScript
compilada pelo Vite. O Node é necessário **apenas para compilar** o
frontend — em produção o Flask serve os arquivos estáticos gerados, sem
nenhum processo Node rodando.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git

# Node 20+ para compilar o frontend (uma vez, e a cada atualização):
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Opcional, só se quiser Redis (ver "Escalando além de um processo"):
# sudo apt install -y redis-server
```

## 2. Get the code and create a dedicated user

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin rpgsys
sudo mkdir -p /opt/rpg_sys
sudo chown rpgsys:rpgsys /opt/rpg_sys
sudo -u rpgsys git clone <your-repo-url> /opt/rpg_sys
cd /opt/rpg_sys
```

## 3. Python environment

```bash
sudo -u rpgsys python3 -m venv /opt/rpg_sys/.venv
sudo -u rpgsys /opt/rpg_sys/.venv/bin/pip install -r requirements.txt
```

## 3b. Compile o frontend

```bash
cd /opt/rpg_sys/frontend
sudo -u rpgsys npm ci
sudo -u rpgsys npm run build      # gera frontend/dist, servido pelo Flask
cd /opt/rpg_sys
```

Se você abrir o site sem ter rodado esse passo, a aplicação responde com
uma página explicando que o frontend não foi compilado.

## 4. Configure

```bash
sudo -u rpgsys cp .env.example .env
sudo -u rpgsys python3 -c "import secrets; print(secrets.token_hex(32))"
# paste the output as SECRET_KEY in .env
sudo -u rpgsys nano .env
```

At minimum set:
- `SECRET_KEY` — a long random value (see command above).
- `DATABASE_PATH` — defaults to `./data/rpg_sys.db`, fine as-is.
- `CORS_ORIGINS` — your real domain, e.g. `https://rpg.example.com`.
- `SESSION_COOKIE_SECURE=1` once HTTPS is set up (step 7).

## 5. Seed the reference data (classes, races, abilities, monsters)

This populates all four built-in systems (medieval fantasy, Call of
Cthulhu, western, cyberpunk). Safe to re-run any time — it upserts.

```bash
sudo -u rpgsys /opt/rpg_sys/.venv/bin/python init_db.py
```

## 6. Run it as a systemd service

```bash
sudo cp deploy/rpg-sys.service /etc/systemd/system/rpg-sys.service
sudo systemctl daemon-reload
sudo systemctl enable --now rpg-sys
sudo systemctl status rpg-sys
```

Logs: `journalctl -u rpg-sys -f`

## 7. Reverse proxy + HTTPS

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/rpg-sys
sudo nano /etc/nginx/sites-available/rpg-sys   # set server_name
sudo ln -s /etc/nginx/sites-available/rpg-sys /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d rpg.example.com
```

After certbot runs, set `SESSION_COOKIE_SECURE=1` in `.env` (if not
already) and `sudo systemctl restart rpg-sys`.

## 8. Play

- Each player opens `https://rpg.example.com` on their own phone/PC and
  registers an account.
- One player creates a session and picks a game system (medieval, Cthulhu,
  western or cyberpunk) — that choice decides which character sheets and
  monster list are available for that table.
- Everyone else creates a character for that same system and joins the
  session from the sessions list.
- The session's creator opens "Entrar como Mestre" to reach the master
  control panel (spawn monsters, adjust HP/resources live, push
  music/images to every connected player).

## Backups

Everything that matters lives in two places:

```
/opt/rpg_sys/data/rpg_sys.db     # characters, sessions, accounts
/opt/rpg_sys/static/uploads/     # uploaded character portraits
/opt/rpg_sys/static/media/       # media the master pushed during sessions
```

A simple nightly cron copying those somewhere else is enough for a
friends'-table game:

```bash
0 4 * * * tar -czf /home/backups/rpg_sys-$(date +\%F).tar.gz -C /opt/rpg_sys data static/uploads static/media
```

## Updating

```bash
cd /opt/rpg_sys
sudo -u rpgsys git pull
sudo -u rpgsys .venv/bin/pip install -r requirements.txt
sudo -u rpgsys sh -c 'cd frontend && npm ci && npm run build'
sudo -u rpgsys .venv/bin/python init_db.py   # picks up any new seed data
sudo systemctl restart rpg-sys
```

## Scaling beyond one process

The SQLite store uses a single writer lock, and Socket.IO needs a shared
message queue once more than one worker process is involved — so the
default single-process setup above is what's tested and recommended for
a normal group's table. If you ever do want more than one worker:

1. `sudo apt install redis-server`
2. Set `REDIS_URL=redis://127.0.0.1:6379/0` in `.env`.
3. Run multiple app processes behind nginx (e.g. via a process manager
   invoking `app.py` on different ports, load-balanced by nginx) — Redis
   makes Socket.IO broadcast correctly across all of them, and session
   cookies are shared via Redis instead of the filesystem.

For the number of players a self-hosted friends' game has, this almost
certainly isn't necessary.

## About the old MongoDB Atlas credentials

Earlier versions of this app connected to a MongoDB Atlas cluster with
credentials hardcoded directly in `conection_db.py`, committed to this
repository's git history. This rewrite removes that dependency entirely
(everything is local now), but the old credentials are still sitting in
your git history. If that Atlas cluster still exists and is reachable
with those credentials, **rotate/delete it** from the MongoDB Atlas
dashboard — being no longer *used* by the code doesn't make it any less
*exposed* in history.

## Desenvolvendo o frontend

Durante o desenvolvimento, rode os dois lados separadamente — o Vite faz
hot-reload e encaminha `/api`, `/static` e `/socket.io` para o Flask:

```bash
# terminal 1
python app.py

# terminal 2
cd frontend && npm run dev     # http://localhost:5173
```

`npm run build` roda `vue-tsc` antes do bundle, então erros de tipo
quebram o build em vez de virarem bug em produção.
