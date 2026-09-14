"""Application configuration, sourced from environment variables.

Every self-hosting-relevant value (database path, Redis URL, allowed
origins, secret key, ...) lives here instead of being hardcoded, so the
same code runs unmodified on a laptop, in Docker, or on a self-hosted
Debian box.
"""
import os

from dotenv import load_dotenv

load_dotenv()


def _split_origins(raw):
    if not raw:
        return "*"
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or "*"


def _bool(name, default=False):
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    # --- Core Flask ---
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = _bool("FLASK_DEBUG", False)
    PREFERRED_URL_SCHEME = os.environ.get("PREFERRED_URL_SCHEME", "https")

    # --- Sessions ---
    # Filesystem sessions are fine for a single-process dev server, but a
    # production deployment (gunicorn with >1 worker, or a reload) needs a
    # shared backend so a user's login/game session is visible everywhere.
    REDIS_URL = os.environ.get("REDIS_URL")
    SESSION_TYPE = "redis" if REDIS_URL else "filesystem"
    SESSION_FILE_DIR = os.environ.get("SESSION_FILE_DIR", "./.flask_session")
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME_MINUTES = int(os.environ.get("SESSION_LIFETIME_MINUTES", "120"))
    SESSION_COOKIE_SECURE = _bool("SESSION_COOKIE_SECURE", not DEBUG)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # --- Database ---
    # A local SQLite-backed document store (see local_db.py) — no external
    # database server required, just a file on disk. Point this at a path
    # under a persistent volume/mount in production.
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "./data/rpg_sys.db")

    # --- Realtime / Socket.IO ---
    # When REDIS_URL is set, Socket.IO uses it as a message queue so events
    # emitted from an HTTP request reach clients connected to a *different*
    # gunicorn worker. Without it, only a single worker process may be used.
    SOCKETIO_MESSAGE_QUEUE = REDIS_URL
    SOCKETIO_ASYNC_MODE = os.environ.get("SOCKETIO_ASYNC_MODE", "gevent")

    # --- CORS / allowed origins ---
    # Comma-separated list, e.g. "https://rpg.example.com,https://www.rpg.example.com"
    CORS_ORIGINS = _split_origins(os.environ.get("CORS_ORIGINS"))

    # --- Uploads ---
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "static/uploads/")
    MEDIA_FOLDER = os.environ.get("MEDIA_FOLDER", "static/media/")
    MUSIC_FOLDER = os.environ.get("MUSIC_FOLDER", "static/music/")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024

    @classmethod
    def validate(cls):
        problems = []
        if not cls.SECRET_KEY:
            problems.append(
                "SECRET_KEY is not set. Generate one with "
                "`python -c \"import secrets; print(secrets.token_hex(32))\"` "
                "and put it in your .env file."
            )
        return problems
