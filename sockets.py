"""Realtime layer: Socket.IO event handlers.

Design notes (this replaces a version that caused most of the reported
sync bugs):

* A single explicit `join_session_room` event is used by *both* the
  player view and the master view to join a session's room. Previously
  the master control page never joined any room at all (it only ever
  relied on Flask's `session['game_session_id']`, which is only set by
  the player-facing `join_session` route) so the master's browser could
  emit updates but could never *receive* live updates back.

* `_connections` maps a Socket.IO session id (`sid`) to who that
  connection belongs to (user id, character id, game session id, master
  flag). Handlers use this registry instead of re-reading Flask's
  cookie-backed `session` object on every event, which is what let stale
  or cross-tab state leak between devices.

* Every mutation is broadcast to the game session's *room* only (never
  to every connected client), so two unrelated tables playing at the
  same time never see each other's music, monsters or character stats.
"""
import logging

from local_db import ObjectId
from flask import request
from flask import session as flask_session
from flask_socketio import emit, join_room, leave_room

from models.character_model import normalize_character
from models.session_model import get_session_by_id, remove_character_from_session

logger = logging.getLogger(__name__)

# sid -> {"user_id": str, "session_id": str, "character_id": str|None, "is_master": bool}
_connections = {}


def _is_master(session_data, user_id):
    return session_data is not None and str(session_data.get("created_by")) == str(user_id)


def _find_users_character_in_session(db, session_data, user_id):
    for char_id in session_data.get("characters", []):
        character = db.chars.find_one({"_id": ObjectId(char_id)})
        if character and str(character.get("user_id")) == str(user_id):
            return character
    return None


def _character_payload(character, class_name, race_name):
    return {
        "_id": str(character["_id"]),
        "name": character["name"],
        "system_id": character.get("system_id", "medieval"),
        "class_name": class_name,
        "race_name": race_name,
        "resources": character.get("resources", {}),
        "img_url": character.get("img_url") or "/static/images/default.png",
    }


def build_session_snapshot(db, session_id):
    """The single source of truth sent to clients on join/reconnect/resync."""
    session_data = get_session_by_id(db, session_id)
    if not session_data:
        return {"session_id": session_id, "characters": [], "monsters": []}

    characters = []
    for char_id in session_data.get("characters", []):
        character = db.chars.find_one({"_id": ObjectId(char_id)})
        if not character:
            continue
        normalize_character(character)
        class_info = db.classes.find_one({"_id": ObjectId(character["class_id"])}) if character.get("class_id") else None
        race_info = db.races.find_one({"_id": ObjectId(character["race_id"])}) if character.get("race_id") else None
        characters.append(_character_payload(
            character,
            class_info["name"] if class_info else "Desconhecido",
            race_info["name"] if race_info else None,
        ))

    monsters = []
    for monster in session_data.get("monsters", []):
        monster = dict(monster)
        monster["current_hp"] = monster.get("current_hp", monster.get("hp", 0))
        monster["current_mana"] = monster.get("current_mana", monster.get("mana", 0))
        monster["current_energia"] = monster.get("current_energia", monster.get("energia", 0))
        monsters.append(monster)

    return {"session_id": session_id, "characters": characters, "monsters": monsters}


def _find_session_id_for_character(db, character_id):
    session_data = db.sessions.find_one({"characters": ObjectId(character_id)})
    return str(session_data["_id"]) if session_data else None


def _broadcast_snapshot(db, socketio, session_id):
    socketio.emit("session_sync", build_session_snapshot(db, session_id), room=session_id)


def register_socket_handlers(socketio, db):

    @socketio.on("connect")
    def on_connect():
        if not flask_session.get("logged_in"):
            return False  # reject the connection
        return True

    @socketio.on("join_session_room")
    def on_join_session_room(data):
        if not flask_session.get("logged_in"):
            return
        user_id = flask_session.get("userId")
        session_id = (data or {}).get("session_id")
        if not user_id or not session_id:
            return

        session_data = get_session_by_id(db, session_id)
        if not session_data:
            emit("session_error", {"message": "Sessão não encontrada."})
            return

        is_master = _is_master(session_data, user_id)
        character_id = None

        if not is_master:
            character = _find_users_character_in_session(db, session_data, user_id)
            if character is None:
                # Not the master and has no character in this session: nothing to join.
                emit("session_error", {"message": "Você não está nesta sessão."})
                return
            character_id = str(character["_id"])

        join_room(session_id)
        _connections[request.sid] = {
            "user_id": user_id,
            "session_id": session_id,
            "character_id": character_id,
            "is_master": is_master,
        }

        # A full, consistent snapshot for everyone in the room beats trying
        # to patch in just the new arrival's data on every other client.
        _broadcast_snapshot(db, socketio, session_id)

    @socketio.on("request_session_sync")
    def on_request_session_sync(data):
        conn = _connections.get(request.sid)
        session_id = (data or {}).get("session_id") or (conn or {}).get("session_id")
        if session_id:
            emit("session_sync", build_session_snapshot(db, session_id))

    @socketio.on("disconnect")
    def on_disconnect():
        conn = _connections.pop(request.sid, None)
        if not conn:
            return
        session_id = conn["session_id"]
        leave_room(session_id)
        if not conn["is_master"] and conn["character_id"]:
            remove_character_from_session(db, session_id, conn["character_id"])
        _broadcast_snapshot(db, socketio, session_id)

    @socketio.on("update_character_status")
    def on_update_character_status(data):
        character_id = data.get("character_id")
        resources = data.get("resources")
        if not character_id or not resources:
            return

        update_fields = {
            f"resources.{key}.current": int(value)
            for key, value in resources.items()
            if value is not None
        }
        if not update_fields:
            return

        db.chars.update_one({"_id": ObjectId(character_id)}, {"$set": update_fields})
        character = normalize_character(db.chars.find_one({"_id": ObjectId(character_id)}))
        session_id = _find_session_id_for_character(db, character_id)
        if not session_id or not character:
            return

        socketio.emit("resources_updated", {
            "character_id": character_id,
            "resources": character.get("resources", {}),
        }, room=session_id)

    @socketio.on("update_monster_stats")
    def on_update_monster_stats(data):
        session_id = data.get("session_id")
        monster_id = data.get("monster_id")
        if not session_id or not monster_id:
            return

        session_data = get_session_by_id(db, session_id)
        if not session_data:
            return

        monsters = session_data.get("monsters", [])
        updated = None
        for monster in monsters:
            if str(monster.get("_id")) == str(monster_id):
                if data.get("hp") is not None:
                    monster["current_hp"] = int(data["hp"])
                if data.get("mana") is not None:
                    monster["current_mana"] = int(data["mana"])
                if data.get("energia") is not None:
                    monster["current_energia"] = int(data["energia"])
                updated = monster
                break

        if updated is None:
            return

        db.sessions.update_one({"_id": ObjectId(session_id)}, {"$set": {"monsters": monsters}})
        socketio.emit("monster_stats_updated", {
            "monster_id": monster_id,
            "current_hp": updated.get("current_hp"),
            "hp": updated.get("hp"),
            "current_mana": updated.get("current_mana"),
            "current_energia": updated.get("current_energia"),
        }, room=session_id)

    @socketio.on("remove_monster")
    def on_remove_monster(data):
        session_id = data.get("session_id")
        monster_id = data.get("monster_id")
        if not session_id or not monster_id:
            return
        db.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$pull": {"monsters": {"_id": monster_id}}},
        )
        socketio.emit("monster_removed", {"monster_id": monster_id}, room=session_id)

    @socketio.on("update_pawn_position")
    def on_update_pawn_position(data):
        conn = _connections.get(request.sid)
        if not conn:
            return
        session_id = conn["session_id"]
        pawn_id = data.get("pawnId")
        x, y = data.get("x"), data.get("y")
        db.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {f"pawns.{pawn_id}.position": {"x": x, "y": y}}},
        )
        socketio.emit("pawn_position_updated", {"pawnId": pawn_id, "x": x, "y": y}, room=session_id)

    @socketio.on("play_music")
    def on_play_music(data):
        session_id = data.get("session_id")
        if session_id:
            socketio.emit("play_music", {"track_url": data.get("track_url")}, room=session_id)

    @socketio.on("stop_music")
    def on_stop_music(data):
        session_id = (data or {}).get("session_id")
        if session_id:
            socketio.emit("stop_music", {}, room=session_id)
