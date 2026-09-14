"""JSON API consumida pelo frontend Vue (frontend/src).

Tudo que a SPA precisa passa por aqui; o Flask não renderiza mais HTML —
só serve o bundle estático e este blueprint. O canal em tempo real
continua sendo o Socket.IO (sockets.py).
"""
import json
import logging
import os
import uuid
from io import BytesIO

from flask import Blueprint, jsonify, request, send_file, session, url_for

from config import Config
from extensions import socketio
from game_systems import DEFAULT_SYSTEM_ID, get_system, system_choices
from local_db import ObjectId
from models.abilities_model import get_abilities_by_system
from models.character_model import (create_character, delete_character,
                                    get_character_by_id,
                                    get_characters_by_user, update_character)
from models.class_model import get_class_by_id, get_classes_by_system
from models.enemies_model import get_enemies_by_system
from models.race_model import (get_art_for_race, get_race_by_id,
                                get_races_by_system)
from models.session_model import (add_character_to_session, create_session,
                                  get_all_sessions, get_session_by_id,
                                  remove_character_from_session)
from models.user_model import create_user, verify_credentials
from pdf_sheet import build_character_sheet_pdf
from serializers import serialize_character as _serialize_character
from sockets import build_session_snapshot

api = Blueprint("api", __name__, url_prefix="/api")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MEDIA_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | {"mp4", "webm"}

db = None  # injetado por init_api()


def init_api(database):
    global db
    db = database
    return api


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def fail(message, status=400):
    return jsonify({"error": message}), status


def current_user_id():
    return session.get("userId") if session.get("logged_in") else None


def login_required(view):
    def wrapper(*args, **kwargs):
        if not current_user_id():
            return fail("Faça login para continuar.", 401)
        return view(*args, **kwargs)

    wrapper.__name__ = view.__name__
    return wrapper


def allowed_file(filename, allowed):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def save_upload(file_storage, folder):
    """Grava o upload com nome aleatório, evitando colisões e path traversal."""
    extension = file_storage.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{extension}"
    os.makedirs(folder, exist_ok=True)
    file_storage.save(os.path.join(folder, filename))
    return "/" + os.path.join(folder, filename).replace(os.sep, "/").lstrip("/")


def serialize_character(character):
    return _serialize_character(db, character)


def session_is_master(session_data, user_id):
    return str(session_data.get("created_by")) == str(user_id)


def user_character_in_session(session_data, user_id):
    for char_id in session_data.get("characters", []):
        character = get_character_by_id(db, char_id)
        if character and str(character.get("user_id")) == str(user_id):
            return character
    return None


# --------------------------------------------------------------------------
# Autenticação
# --------------------------------------------------------------------------

@api.post("/auth/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return fail("Usuário e senha são obrigatórios.")

    user_id = create_user(db, username, password)
    if user_id is None:
        return fail("Esse usuário já existe.", 409)

    session.clear()
    session["logged_in"] = True
    session["userId"] = user_id
    session["username"] = username
    session.permanent = True
    return jsonify({"user": {"id": user_id, "username": username}})


@api.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    user = verify_credentials(db, data.get("username", ""), data.get("password", ""))
    if not user:
        return fail("Usuário ou senha inválidos.", 401)

    session.clear()
    session["logged_in"] = True
    session["userId"] = str(user["_id"])
    session["username"] = user["username"]
    session.permanent = True
    return jsonify({"user": {"id": str(user["_id"]), "username": user["username"]}})


@api.post("/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@api.get("/auth/me")
def me():
    if not current_user_id():
        return jsonify({"user": None})
    return jsonify({"user": {"id": session["userId"], "username": session.get("username")}})


# --------------------------------------------------------------------------
# Sistemas de RPG
# --------------------------------------------------------------------------

@api.get("/systems")
def list_systems():
    return jsonify({"systems": system_choices()})


@api.get("/systems/<system_id>/options")
@login_required
def system_options(system_id):
    system = get_system(system_id)
    races = get_races_by_system(db, system_id) if system["uses_race"] else []

    return jsonify({
        "classes": [
            {
                "_id": str(item["_id"]),
                "name": item["name"],
                "resource_bases": item.get("resource_bases", {}),
                "combat_bases": item.get("combat_bases", {}),
                "pericias": item.get("pericias", {}),
                "habilidades_classe": item.get("habilidades_classe", {}),
            }
            for item in get_classes_by_system(db, system_id)
        ],
        "races": [
            {
                "_id": str(item["_id"]),
                "name": item["name"],
                "resumo": item.get("resumo", ""),
                "img_url": item.get("img_url") or get_art_for_race(item["name"]),
                "attribute_bonuses": item.get("attribute_bonuses", {}),
                "resource_bonuses": item.get("resource_bonuses", {}),
                "habilidades_inatas": item.get("habilidades_inatas", {}),
            }
            for item in races
        ],
        "abilities": [
            {
                "id": str(item["_id"]),
                "name": item["name"],
                "description": item.get("description", ""),
                "cost": item.get("cost", {}),
                "icon": item.get("icon"),
            }
            for item in get_abilities_by_system(db, system_id)
        ],
    })


# --------------------------------------------------------------------------
# Personagens
# --------------------------------------------------------------------------

def _parse_character_form():
    form = request.form
    system_id = form.get("system_id", DEFAULT_SYSTEM_ID)
    system = get_system(system_id)

    try:
        attributes = json.loads(form.get("attributes") or "{}")
        pericias = json.loads(form.get("pericias") or "[]")
        habilidades = json.loads(form.get("habilidades") or "[]")
    except json.JSONDecodeError:
        return None, fail("Dados do personagem malformados.")

    name = (form.get("name") or "").strip()
    if not name:
        return None, fail("Dê um nome ao personagem.")

    class_id = form.get("class_id")
    if not class_id:
        return None, fail(f"Escolha {system['class_label'].lower()}.")

    race_id = form.get("race_id") if system["uses_race"] else None
    if system["uses_race"] and not race_id:
        return None, fail(f"Escolha {system['race_label'].lower()}.")

    if len(habilidades) > 5:
        return None, fail(f"No máximo 5 {system['ability_label'].lower()}.")
    if len(pericias) > 3:
        return None, fail(f"No máximo 3 {system['skill_label'].lower()}.")

    base_attributes = {}
    for attr in system["attributes"]:
        try:
            base_attributes[attr["key"]] = int(attributes.get(attr["key"], 10))
        except (TypeError, ValueError):
            return None, fail(f"Valor inválido para {attr['label']}.")

    return {
        "system_id": system_id,
        "name": name,
        "class_id": class_id,
        "race_id": race_id,
        "origem": form.get("origem", ""),
        "attributes": base_attributes,
        "pericias": pericias,
        "habilidades": habilidades,
    }, None


@api.get("/characters")
@login_required
def list_characters():
    characters = get_characters_by_user(db, current_user_id())
    return jsonify({"characters": [serialize_character(c) for c in characters]})


@api.get("/characters/<character_id>")
@login_required
def read_character(character_id):
    character = get_character_by_id(db, character_id)
    if not character:
        return fail("Personagem não encontrado.", 404)
    return jsonify({"character": serialize_character(character)})


@api.post("/characters")
@login_required
def create_character_route():
    payload, error = _parse_character_form()
    if error:
        return error

    img_url = None
    upload = request.files.get("image")
    if upload and upload.filename:
        if not allowed_file(upload.filename, ALLOWED_IMAGE_EXTENSIONS):
            return fail("Formato de imagem não suportado. Use PNG, JPG ou WEBP.")
        img_url = save_upload(upload, Config.UPLOAD_FOLDER)

    character = create_character(
        db,
        current_user_id(),
        payload["system_id"],
        payload["name"],
        payload["class_id"],
        payload["race_id"],
        img_url,
        payload["attributes"],
        payload["origem"],
        pericias_selecionadas=payload["pericias"],
        habilidades_selecionadas=payload["habilidades"],
    )
    return jsonify({"character": serialize_character(character)})


@api.post("/characters/<character_id>")
@login_required
def update_character_route(character_id):
    existing = get_character_by_id(db, character_id)
    if not existing or str(existing["user_id"]) != current_user_id():
        return fail("Personagem não encontrado.", 404)

    payload, error = _parse_character_form()
    if error:
        return error

    img_url = existing.get("img_url")
    upload = request.files.get("image")
    if upload and upload.filename:
        if not allowed_file(upload.filename, ALLOWED_IMAGE_EXTENSIONS):
            return fail("Formato de imagem não suportado.")
        img_url = save_upload(upload, Config.UPLOAD_FOLDER)

    habilidades = {}
    for ability_name in payload["habilidades"]:
        ability = db.abilities.find_one({"name": ability_name, "system_id": payload["system_id"]})
        if ability:
            habilidades[str(ability["_id"])] = {
                "name": ability["name"],
                "description": ability.get("description", ""),
                "cost": ability.get("cost", {}),
                "icon": ability.get("icon"),
            }

    update_character(
        db, character_id, payload["name"], payload["class_id"],
        payload["race_id"], img_url, payload["origem"],
    )
    db.chars.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": {
            "pericias": {skill: 4 for skill in payload["pericias"]},
            "habilidades": habilidades,
        }},
    )

    return jsonify({"character": serialize_character(get_character_by_id(db, character_id))})


@api.delete("/characters/<character_id>")
@login_required
def delete_character_route(character_id):
    character = get_character_by_id(db, character_id)
    if not character or str(character["user_id"]) != current_user_id():
        return fail("Personagem não encontrado.", 404)
    delete_character(db, character_id)
    return jsonify({"ok": True})


@api.post("/characters/<character_id>/use-ability")
@login_required
def use_ability(character_id):
    data = request.get_json(silent=True) or {}
    character = get_character_by_id(db, character_id)
    if not character or str(character["user_id"]) != current_user_id():
        return fail("Personagem não encontrado.", 404)

    ability = (character.get("habilidades") or {}).get(str(data.get("ability_id")))
    if not ability:
        return fail("Habilidade não encontrada nesta ficha.", 404)

    resources = character.get("resources", {})
    cost = ability.get("cost", {})

    for key, amount in cost.items():
        if resources.get(key, {}).get("current", 0) < amount:
            return fail("Recursos insuficientes para usar esta habilidade.")

    updates = {}
    for key, amount in cost.items():
        if not amount:
            continue
        resources[key]["current"] -= amount
        updates[f"resources.{key}.current"] = resources[key]["current"]

    if updates:
        db.chars.update_one({"_id": ObjectId(character_id)}, {"$set": updates})

    game_session = db.sessions.find_one({"characters": ObjectId(character_id)})
    if game_session:
        socketio.emit(
            "resources_updated",
            {"character_id": str(character["_id"]), "resources": resources},
            room=str(game_session["_id"]),
        )

    return jsonify({"resources": resources})


@api.get("/characters/<character_id>/pdf")
@login_required
def character_pdf(character_id):
    character = get_character_by_id(db, character_id)
    if not character:
        return fail("Personagem não encontrado.", 404)

    class_info = get_class_by_id(db, character["class_id"]) if character.get("class_id") else None
    race_info = get_race_by_id(db, character["race_id"]) if character.get("race_id") else None

    buffer = BytesIO()
    build_character_sheet_pdf(buffer, character, class_info, race_info)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{character['name']}_Ficha.pdf",
        mimetype="application/pdf",
    )


# --------------------------------------------------------------------------
# Mesas
# --------------------------------------------------------------------------

@api.get("/sessions")
@login_required
def list_sessions():
    user_id = current_user_id()
    result = []
    for game_session in get_all_sessions(db):
        creator = db.users.find_one({"_id": game_session["created_by"]})
        result.append({
            "_id": str(game_session["_id"]),
            "name": game_session["name"],
            "system_id": game_session.get("system_id", DEFAULT_SYSTEM_ID),
            "creator_name": creator["username"] if creator else "Desconhecido",
            "is_master": session_is_master(game_session, user_id),
            "player_count": len(game_session.get("characters", [])),
        })
    return jsonify({"sessions": result})


@api.post("/sessions")
@login_required
def create_session_route():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return fail("Dê um nome à mesa.")

    system_id = data.get("system_id", DEFAULT_SYSTEM_ID)
    session_id = create_session(db, name, current_user_id(), system_id)

    return jsonify({
        "session": {
            "_id": str(session_id),
            "name": name,
            "system_id": system_id,
            "creator_name": session.get("username", ""),
            "is_master": True,
            "player_count": 0,
        }
    })


@api.delete("/sessions/<session_id>")
@login_required
def delete_session_route(session_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)
    if not session_is_master(game_session, current_user_id()):
        return fail("Apenas o Mestre pode excluir a mesa.", 403)

    db.sessions.delete_one({"_id": ObjectId(session_id)})
    return jsonify({"ok": True})


@api.get("/sessions/<session_id>")
@login_required
def read_session(session_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)

    user_id = current_user_id()
    system_id = game_session.get("system_id", DEFAULT_SYSTEM_ID)
    mine = [c for c in get_characters_by_user(db, user_id) if c.get("system_id") == system_id]
    joined = user_character_in_session(game_session, user_id)
    creator = db.users.find_one({"_id": game_session["created_by"]})

    return jsonify({
        "session": {
            "_id": str(game_session["_id"]),
            "name": game_session["name"],
            "system_id": system_id,
            "creator_name": creator["username"] if creator else "Desconhecido",
        },
        "is_master": session_is_master(game_session, user_id),
        "my_characters": [serialize_character(c) for c in mine],
        "my_character_id": str(joined["_id"]) if joined else None,
    })


@api.post("/sessions/<session_id>/join")
@login_required
def join_session_route(session_id):
    data = request.get_json(silent=True) or {}
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)

    character = get_character_by_id(db, data.get("character_id"))
    if not character or str(character["user_id"]) != current_user_id():
        return fail("Personagem inválido.", 404)

    if character.get("system_id") != game_session.get("system_id", DEFAULT_SYSTEM_ID):
        return fail("Este personagem é de outro sistema de RPG.")

    already = [str(c) for c in game_session.get("characters", [])]
    if str(character["_id"]) not in already:
        add_character_to_session(db, session_id, character["_id"])
        socketio.emit("session_sync", build_session_snapshot(db, session_id), room=session_id)

    return jsonify({"ok": True})


@api.get("/sessions/<session_id>/table")
@login_required
def table_bootstrap(session_id):
    """Dados mínimos para a SPA montar o lobby; o resto chega pelo socket."""
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)

    user_id = current_user_id()
    character = user_character_in_session(game_session, user_id)
    if not character and not session_is_master(game_session, user_id):
        return fail("Você não está nesta mesa.", 403)

    return jsonify({
        "system_id": game_session.get("system_id", DEFAULT_SYSTEM_ID),
        "session_name": game_session["name"],
        "character_id": str(character["_id"]) if character else None,
        "is_master": session_is_master(game_session, user_id),
    })


@api.get("/sessions/<session_id>/master")
@login_required
def master_bootstrap(session_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)
    if not session_is_master(game_session, current_user_id()):
        return fail("Apenas o Mestre acessa este painel.", 403)

    system_id = game_session.get("system_id", DEFAULT_SYSTEM_ID)
    return jsonify({
        "session": {
            "_id": str(game_session["_id"]),
            "name": game_session["name"],
            "system_id": system_id,
        },
        "enemies": [
            {
                "_id": str(enemy["_id"]),
                "name": enemy["name"],
                "hp": enemy.get("hp", 0),
                "resumo": enemy.get("resumo", ""),
            }
            for enemy in get_enemies_by_system(db, system_id)
        ],
    })


@api.post("/sessions/<session_id>/monsters")
@login_required
def spawn_monsters(session_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)
    if not session_is_master(game_session, current_user_id()):
        return fail("Apenas o Mestre pode invocar criaturas.", 403)

    data = request.get_json(silent=True) or {}
    template = db.enemies.find_one({"_id": ObjectId(str(data.get("monster_id")))})
    if not template:
        return fail("Criatura não encontrada.", 404)

    quantity = max(1, min(int(data.get("quantity", 1)), 12))
    created = []
    for _ in range(quantity):
        monster = {
            "_id": str(ObjectId()),
            "name": template["name"],
            "hp": template["hp"],
            "current_hp": template["hp"],
            "mana": template.get("mana", 0),
            "current_mana": template.get("mana", 0),
            "energia": template.get("energia", 0),
            "current_energia": template.get("energia", 0),
            "resumo": template.get("resumo", ""),
            "ataque": template.get("ataque", 0),
            "defesa": template.get("defesa", 0),
            "img_url": template.get("img_url", "default.png"),
            "spawn_som": template.get("spawn_som", ""),
        }
        db.sessions.update_one({"_id": ObjectId(session_id)}, {"$push": {"monsters": monster}})
        socketio.emit("monster_added", monster, room=session_id)
        created.append(monster)

    return jsonify({"monsters": created})


@api.post("/sessions/<session_id>/players/<character_id>/kick")
@login_required
def kick_player(session_id, character_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)
    if not session_is_master(game_session, current_user_id()):
        return fail("Apenas o Mestre pode remover jogadores.", 403)

    remove_character_from_session(db, session_id, character_id)
    socketio.emit("session_sync", build_session_snapshot(db, session_id), room=session_id)
    return jsonify({"ok": True})


# --------------------------------------------------------------------------
# Trilha sonora e mídia (sempre restritas à sala da mesa)
# --------------------------------------------------------------------------

@api.get("/music")
@login_required
def music_tracks():
    folder = Config.MUSIC_FOLDER
    tracks = []
    if os.path.isdir(folder):
        for filename in sorted(os.listdir(folder)):
            if filename.lower().endswith(("mp3", "wav", "ogg")):
                tracks.append({
                    "name": filename.rsplit(".", 1)[0],
                    "url": url_for("static", filename=f"music/{filename}"),
                })
    return jsonify({"tracks": tracks})


@api.post("/sessions/<session_id>/music")
@login_required
def control_music(session_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)
    if not session_is_master(game_session, current_user_id()):
        return fail("Apenas o Mestre controla a trilha sonora.", 403)

    track_url = (request.get_json(silent=True) or {}).get("track_url")
    if not track_url:
        socketio.emit("stop_music", {}, room=session_id)
        return jsonify({"ok": True})

    relative = track_url.replace("/static/", "", 1)
    if ".." in relative or not os.path.exists(os.path.join("static", relative)):
        return fail("Faixa não encontrada.", 404)

    socketio.emit("play_music", {"track_url": track_url}, room=session_id)
    return jsonify({"ok": True})


@api.post("/sessions/<session_id>/media")
@login_required
def push_media(session_id):
    game_session = get_session_by_id(db, session_id)
    if not game_session:
        return fail("Mesa não encontrada.", 404)
    if not session_is_master(game_session, current_user_id()):
        return fail("Apenas o Mestre pode enviar mídia.", 403)

    upload = request.files.get("media")
    if not upload or not upload.filename:
        return fail("Escolha um arquivo.")
    if not allowed_file(upload.filename, ALLOWED_MEDIA_EXTENSIONS):
        return fail("Formato não suportado.")

    media_url = save_upload(upload, Config.MEDIA_FOLDER)
    display_time = request.form.get("display_time", type=int)

    socketio.emit(
        "new_media",
        {"media_url": media_url, "display_time": display_time},
        room=session_id,
    )
    logging.info("Mídia enviada para a mesa %s", session_id)
    return jsonify({"ok": True, "media_url": media_url})
