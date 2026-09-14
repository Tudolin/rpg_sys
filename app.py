from gevent import monkey

monkey.patch_all()

import logging
import os
from datetime import timedelta

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from api import init_api
from conection_db import connection
from config import Config
from extensions import socketio
from flask_session import Session
from sockets import register_socket_handlers

logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)

for problem in Config.validate():
    logging.warning(problem)

# O frontend é uma SPA Vue compilada pelo Vite (ver frontend/). Em produção
# servimos o bundle estático daqui — nenhum processo Node roda no servidor.
SPA_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "dist")

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
    minutes=Config.PERMANENT_SESSION_LIFETIME_MINUTES
)
Session(app)

CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

db = connection()

socketio.init_app(app)
register_socket_handlers(socketio, db)
app.register_blueprint(init_api(db))


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.get("/assets/<path:filename>")
def spa_assets(filename):
    """Bundles com hash no nome — podem ser cacheados agressivamente."""
    response = send_from_directory(os.path.join(SPA_DIST, "assets"), filename)
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


@app.get("/", defaults={"path": ""})
@app.get("/<path:path>")
def spa(path):
    """Entrega o index.html da SPA; o roteamento fica a cargo do Vue Router."""
    if path and os.path.isfile(os.path.join(SPA_DIST, path)):
        return send_from_directory(SPA_DIST, path)

    index = os.path.join(SPA_DIST, "index.html")
    if not os.path.isfile(index):
        return (
            "<h1>Frontend não compilado</h1>"
            "<p>Rode <code>npm install && npm run build</code> dentro de "
            "<code>frontend/</code> e recarregue esta página.</p>",
            503,
        )
    return send_from_directory(SPA_DIST, "index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        debug=Config.DEBUG,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 8000)),
    )
