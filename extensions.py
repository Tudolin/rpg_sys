"""Shared extension instances, created once and imported everywhere else.

Keeping this separate from app.py avoids circular imports between
app.py, sockets.py and the route modules.
"""
from flask_socketio import SocketIO

from config import Config

socketio = SocketIO(
    cors_allowed_origins=Config.CORS_ORIGINS,
    async_mode=Config.SOCKETIO_ASYNC_MODE,
    message_queue=Config.SOCKETIO_MESSAGE_QUEUE,
)
