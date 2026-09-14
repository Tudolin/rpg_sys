from gevent import monkey

monkey.patch_all()

import json
import logging
import os
import uuid
from datetime import timedelta
from io import BytesIO

from local_db import ObjectId
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_file, session, url_for)
from flask_cors import CORS
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from conection_db import connection
from config import Config
from extensions import socketio
from flask_session import Session
from game_systems import DEFAULT_SYSTEM_ID, get_system, system_choices
from models.abilities_model import get_abilities_by_system
from models.character_model import (create_character, delete_character,
                                    get_character_by_id,
                                    get_characters_by_user, update_character)
from models.class_model import get_class_by_id, get_classes_by_system
from models.enemies_model import get_enemies_by_system
from models.race_model import get_race_by_id, get_races_by_system
from models.session_model import (add_character_to_session, create_session,
                                  get_all_sessions, get_session_by_id,
                                  remove_character_from_session)
from models.user_model import create_user, verify_credentials
from sockets import build_session_snapshot, register_socket_handlers

logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)

for problem in Config.validate():
    logging.warning(problem)

app = Flask(__name__)
app.config.from_object(Config)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=Config.PERMANENT_SESSION_LIFETIME_MINUTES)
Session(app)

CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

db = connection()

socketio.init_app(app)
register_socket_handlers(socketio, db)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MEDIA_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | {"mp4", "webm"}


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_upload(file_storage, folder):
    """Save an uploaded file under a random name to avoid clobbering/collisions."""
    extension = file_storage.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(folder, filename)
    file_storage.save(file_path)
    return file_path


def require_login():
    return session.get("logged_in")


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    if not require_login():
        return redirect(url_for("login"))

    characters = get_characters_by_user(db, session["userId"])
    for char in characters:
        char["system"] = get_system(char["system_id"])
    return render_template("home.html", characters=characters)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = verify_credentials(db, username, password)
        if user:
            session.clear()
            session["logged_in"] = True
            session["userId"] = str(user["_id"])
            session["username"] = user["username"]
            session.permanent = True
            return redirect(url_for("home"))

        flash("Credenciais inválidas.", "danger")
        return render_template("login.html", error="Credenciais inválidas")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return render_template("register.html", error="Usuário e senha são obrigatórios.")

        user_id = create_user(db, username, password)
        if user_id is None:
            return render_template("register.html", error="Usuário já existe")

        session.clear()
        session["logged_in"] = True
        session["userId"] = user_id
        session["username"] = username
        session.permanent = True
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    try:
        game_session_id = session.get("game_session_id")
        character_id = session.get("character_id")
        if game_session_id and character_id:
            remove_character_from_session(db, game_session_id, character_id)
            socketio.emit("session_sync", build_session_snapshot(db, game_session_id), room=game_session_id)
    except Exception as e:
        logging.error("Erro ao remover personagem da sessão no logout: %s", e)

    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------

def _build_habilidades_disponiveis(system_id):
    system = get_system(system_id)
    abilities = get_abilities_by_system(db, system_id)
    return [
        {
            "id": str(ability["_id"]),
            "nome": ability["name"],
            "descricao": ability["description"],
            "custo": ability.get("cost", {}),
        }
        for ability in abilities
    ], system


def _classes_data_for_js(classes):
    return {
        str(cls["_id"]): {
            "name": cls["name"],
            "resource_bases": cls.get("resource_bases", {}),
            "combat_bases": cls.get("combat_bases", {}),
            "pericias": cls.get("pericias", {}),
        }
        for cls in classes
    }


def _races_data_for_js(races):
    return {
        str(race["_id"]): {
            "name": race["name"],
            "attribute_bonuses": race.get("attribute_bonuses", {}),
            "resource_bonuses": race.get("resource_bonuses", {}),
            "resumo": race.get("resumo", ""),
        }
        for race in races
    }


@app.route("/create_character", methods=["GET", "POST"])
def create_character_route():
    if not require_login():
        return redirect(url_for("login"))

    system_id = request.values.get("system", DEFAULT_SYSTEM_ID)
    system = get_system(system_id)
    classes = get_classes_by_system(db, system_id)
    races = get_races_by_system(db, system_id) if system["uses_race"] else []
    habilidades_disponiveis, _ = _build_habilidades_disponiveis(system_id)

    if request.method == "POST":
        name = request.form["name"].strip()
        class_id = request.form.get("class_id")
        race_id = request.form.get("race_id") if system["uses_race"] else None
        origem = request.form.get("origem", "")

        if not name or not class_id or (system["uses_race"] and not race_id):
            return f"Nome, {system['class_label']} e {system.get('race_label') or ''} são obrigatórios.", 400

        base_attributes = {}
        for attr in system["attributes"]:
            try:
                base_attributes[attr["key"]] = int(request.form.get(attr["key"], 0))
            except ValueError:
                return f"Valor inválido para o atributo {attr['label']}.", 400

        pericias_selecionadas = request.form.getlist("pericias")
        habilidades_selecionadas = json.loads(request.form.get("habilidades_selecionadas", "[]"))

        if len(habilidades_selecionadas) > 5:
            return f"Você pode selecionar no máximo 5 {system['ability_label'].lower()}.", 400

        img_url = None
        if "img_url" in request.files and request.files["img_url"].filename:
            file = request.files["img_url"]
            if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                return "Formato de imagem não suportado. Use PNG, JPG ou WEBP.", 400
            img_url = save_upload(file, app.config["UPLOAD_FOLDER"])

        create_character(
            db, session["userId"], system_id, name, class_id, race_id, img_url,
            base_attributes, origem,
            pericias_selecionadas=pericias_selecionadas,
            habilidades_selecionadas=habilidades_selecionadas,
        )
        return redirect(url_for("home"))

    return render_template(
        "create_character.html",
        classes=classes, races=races,
        habilidades_disponiveis=habilidades_disponiveis,
        classes_data=_classes_data_for_js(classes),
        races_data=_races_data_for_js(races),
        system=system, system_choices=system_choices(),
    )


@app.route("/edit_character/<character_id>", methods=["GET", "POST"])
def edit_character_route(character_id):
    if not require_login():
        return redirect(url_for("login"))

    character = get_character_by_id(db, character_id)
    if not character or str(character["user_id"]) != session["userId"]:
        return redirect(url_for("home"))

    system_id = character["system_id"]
    system = get_system(system_id)

    char_race_info = get_race_by_id(db, character["race_id"]) if character.get("race_id") else None
    race_name = char_race_info["name"] if char_race_info else None

    classes = get_classes_by_system(db, system_id)
    races = get_races_by_system(db, system_id) if system["uses_race"] else []
    habilidades_disponiveis, _ = _build_habilidades_disponiveis(system_id)

    if request.method == "POST":
        name = request.form["name"].strip()
        class_id = request.form["class_id"]
        race_id = request.form.get("race_id") if system["uses_race"] else None
        origem = request.form.get("origem", "")

        img_url = character.get("img_url")
        if "img_url" in request.files and request.files["img_url"].filename:
            file = request.files["img_url"]
            if allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                img_url = save_upload(file, app.config["UPLOAD_FOLDER"])

        habilidades_selecionadas = json.loads(request.form.get("habilidades_selecionadas", "[]"))
        if len(habilidades_selecionadas) > 5:
            return f"Você pode selecionar no máximo 5 {system['ability_label'].lower()}.", 400

        habilidades = {}
        for habilidade_nome in habilidades_selecionadas:
            habilidade = db.abilities.find_one({"name": habilidade_nome, "system_id": system_id})
            if habilidade:
                habilidades[str(habilidade["_id"])] = {
                    "name": habilidade["name"],
                    "description": habilidade["description"],
                    "cost": habilidade.get("cost", {}),
                    "icon": habilidade.get("icon"),
                }

        pericias_selecionadas = request.form.getlist("pericias")
        pericias = {pericia: 4 for pericia in pericias_selecionadas}

        update_character(db, character_id, name, class_id, race_id, img_url, origem)
        db.chars.update_one(
            {"_id": ObjectId(character_id)},
            {"$set": {"pericias": pericias, "habilidades": habilidades}},
        )

        return redirect(url_for("home"))

    return render_template(
        "edit_character.html",
        character=character, classes=classes, races=races,
        habilidades_disponiveis=habilidades_disponiveis,
        classes_data=_classes_data_for_js(classes),
        race_name=race_name, system=system,
        selected_habilidades=[h["name"] for h in character.get("habilidades", {}).values()],
        selected_pericias=list(character.get("pericias", {}).keys()),
    )


@app.route("/delete_character/<character_id>")
def delete_character_route(character_id):
    if not require_login():
        return redirect(url_for("login"))

    character = get_character_by_id(db, character_id)
    if character and str(character["user_id"]) == session["userId"]:
        delete_character(db, character_id)
    return redirect(url_for("home"))


# ---------------------------------------------------------------------------
# Sessions / lobby
# ---------------------------------------------------------------------------

@app.route("/sessions", methods=["GET", "POST"])
def sessions():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        session_name = request.form["session_name"].strip()
        system_id = request.form.get("system_id", DEFAULT_SYSTEM_ID)
        if session_name:
            create_session(db, session_name, session["userId"], system_id)
        return redirect(url_for("sessions"))

    all_sessions = list(get_all_sessions(db))
    for sess in all_sessions:
        user = db.users.find_one({"_id": sess["created_by"]})
        sess["creator_name"] = user["username"] if user else "Desconhecido"
        sess["created_by"] = str(sess["created_by"])
        sess["userId"] = session["userId"]
        sess["system"] = get_system(sess.get("system_id"))

    return render_template("sessions.html", sessions=all_sessions, system_choices=system_choices())


@app.route("/delete_session/<session_id>", methods=["POST"])
def delete_session(session_id):
    if not require_login():
        return redirect(url_for("login"))

    session_data = get_session_by_id(db, session_id)
    if session_data and session_data["created_by"] == ObjectId(session["userId"]):
        db.sessions.delete_one({"_id": ObjectId(session_id)})
        flash("Sessão excluída com sucesso.", "success")
    else:
        flash("Você não tem permissão para excluir esta sessão.", "danger")

    return redirect(url_for("sessions"))


@app.route("/join_session/<session_id>", methods=["GET", "POST"])
def join_session(session_id):
    if not require_login():
        return redirect(url_for("login"))

    session_data = get_session_by_id(db, session_id)
    if not session_data:
        flash("Sessão não encontrada.", "danger")
        return redirect(url_for("sessions"))

    system_id = session_data["system_id"]
    all_characters = get_characters_by_user(db, session["userId"])
    # A character built for one ruleset can't join a table running another.
    characters = [c for c in all_characters if c["system_id"] == system_id]

    if request.method == "POST":
        character_id = request.form["character_id"]

        if character_id in [str(c) for c in session_data.get("characters", [])]:
            flash("Este personagem já está na sessão.", "danger")
            return redirect(url_for("game_lobby"))

        add_character_to_session(db, session_id, character_id)
        session["game_session_id"] = session_id
        session["character_id"] = character_id

        socketio.emit("session_sync", build_session_snapshot(db, session_id), room=session_id)
        return redirect(url_for("game_lobby"))

    return render_template(
        "join_session.html", characters=characters,
        session_name=session_data.get("name", "Sessão Desconhecida"),
        session_data=session_data, system=get_system(system_id),
        is_master=str(session_data["created_by"]) == session["userId"],
    )


@app.route("/game_lobby")
def game_lobby():
    if not require_login() or "game_session_id" not in session:
        return redirect(url_for("login"))

    session_id = session["game_session_id"]
    session_data = get_session_by_id(db, session_id)
    if not session_data:
        session.pop("game_session_id", None)
        return redirect(url_for("sessions"))

    character_id = session.get("character_id")
    character = get_character_by_id(db, character_id) if character_id else None
    if not character:
        character = db.chars.find_one({
            "user_id": ObjectId(session["userId"]),
            "_id": {"$in": [ObjectId(c) for c in session_data.get("characters", [])]},
        })
        if character:
            from models.character_model import normalize_character
            normalize_character(character)
            session["character_id"] = str(character["_id"])

    if not character:
        return redirect(url_for("home"))

    system = get_system(character["system_id"])

    class_info = get_class_by_id(db, character["class_id"]) if character.get("class_id") else None
    race_info = get_race_by_id(db, character["race_id"]) if character.get("race_id") else None
    character["class_name"] = class_info["name"] if class_info else "Desconhecido"
    character["race_name"] = race_info["name"] if race_info else None

    habilidades_formatadas = []
    for habilidade_id, habilidade_data in character.get("habilidades", {}).items():
        if isinstance(habilidade_data, dict):
            habilidades_formatadas.append({
                "id": habilidade_id,
                "name": habilidade_data.get("name"),
                "description": habilidade_data.get("description"),
                "cost": habilidade_data.get("cost", {}),
                "icon": habilidade_data.get("icon"),
            })
    character["habilidades"] = habilidades_formatadas
    character["pericias"] = character.get("pericias", {})

    other_characters = []
    for char_id in session_data.get("characters", []):
        if str(char_id) == str(character["_id"]):
            continue
        char = get_character_by_id(db, char_id)
        if not char:
            continue
        char_class = get_class_by_id(db, char["class_id"]) if char.get("class_id") else None
        char_race = get_race_by_id(db, char["race_id"]) if char.get("race_id") else None
        char["class_name"] = char_class["name"] if char_class else "Desconhecido"
        char["race_name"] = char_race["name"] if char_race else None
        other_characters.append(char)

    monsters = session_data.get("monsters", [])

    return render_template(
        "game_lobby.html", character=character, other_characters=other_characters,
        session_name=session_data["name"], monsters=monsters,
        system=system, session_id=session_id,
    )


# ---------------------------------------------------------------------------
# Master control
# ---------------------------------------------------------------------------

@app.route("/master_control/<session_id>", methods=["GET", "POST"])
def master_control(session_id):
    if not require_login():
        return redirect(url_for("login"))

    session_data = get_session_by_id(db, session_id)
    if not session_data:
        flash("Sessão não encontrada.", "danger")
        return redirect(url_for("sessions"))

    if session_data["created_by"] != ObjectId(session["userId"]):
        flash("Apenas o Mestre da sessão pode acessar essa página.", "danger")
        return redirect(url_for("home"))

    system = get_system(session_data["system_id"])
    characters = [get_character_by_id(db, c) for c in session_data.get("characters", [])]
    characters = [c for c in characters if c]
    monsters = session_data.get("monsters", [])

    if request.method == "POST":
        if "char_id" in request.form:
            char_id = request.form["char_id"]
            update_fields = {}
            for res in system["resources"]:
                raw_value = request.form.get(f"resource_{res['key']}")
                if raw_value is not None and raw_value != "":
                    update_fields[f"resources.{res['key']}.current"] = int(raw_value)

            if update_fields:
                db.chars.update_one({"_id": ObjectId(char_id)}, {"$set": update_fields})
                socketio.emit("session_sync", build_session_snapshot(db, session_id), room=session_id)
                flash("Status do personagem atualizado com sucesso!", "success")

            return redirect(url_for("master_control", session_id=session_id))

        elif "monster_id" in request.form:
            monster_id = request.form["monster_id"]
            quantity = int(request.form.get("quantity", 1))
            _add_monsters_to_session(session_id, monster_id, quantity)
            return redirect(url_for("master_control", session_id=session_id))

    enemies = get_enemies_by_system(db, session_data["system_id"])

    return render_template(
        "master_control.html", characters=characters, session_data=session_data,
        session_name=session_data["name"], enemies=enemies, monsters=monsters,
        session_id=session_id, system=system,
    )


def _add_monsters_to_session(session_id, monster_id, quantity):
    created = []
    monster = db.enemies.find_one({"_id": ObjectId(monster_id)})
    if not monster:
        return created

    for _ in range(max(1, quantity)):
        new_monster = {
            "_id": str(ObjectId()),
            "name": monster["name"],
            "hp": monster["hp"],
            "current_hp": monster["hp"],
            "mana": monster.get("mana", 0),
            "current_mana": monster.get("mana", 0),
            "energia": monster.get("energia", 0),
            "current_energia": monster.get("energia", 0),
            "resumo": monster.get("resumo", ""),
            "ataque": monster.get("ataque", 0),
            "defesa": monster.get("defesa", 0),
            "img_url": monster.get("img_url", "default.png"),
            "spawn_som": monster.get("spawn_som", "default.mp3"),
        }
        db.sessions.update_one({"_id": ObjectId(session_id)}, {"$push": {"monsters": new_monster}})
        socketio.emit("monster_added", new_monster, room=session_id)
        created.append(new_monster)

    return created


@app.route("/add_monster_to_session", methods=["POST"])
def add_monster_to_session():
    if not require_login():
        return jsonify({"success": False, "message": "Usuário não logado"}), 401

    data = request.get_json(force=True, silent=True) or {}
    session_id = data.get("session_id")
    monster_id = data.get("monster_id")
    quantity = int(data.get("quantity", 1))

    if not session_id or not monster_id:
        return jsonify({"success": False, "message": "Dados insuficientes para adicionar o monstro"}), 400

    session_data = get_session_by_id(db, session_id)
    if not session_data:
        return jsonify({"success": False, "message": "Sessão não encontrada"}), 404

    if session_data["created_by"] != ObjectId(session["userId"]):
        return jsonify({"success": False, "message": "Apenas o mestre da sessão pode adicionar monstros"}), 403

    created = _add_monsters_to_session(session_id, monster_id, quantity)
    if not created:
        return jsonify({"success": False, "message": "Monstro não encontrado"}), 404

    return jsonify({"success": True, "monsters": created})


@app.route("/remove_player/<char_id>", methods=["POST"])
def remove_player(char_id):
    if not require_login():
        return jsonify({"success": False, "error": "Not logged in"}), 403

    body = request.get_json(silent=True) or {}
    session_id = body.get("session_id") or session.get("game_session_id")
    if not session_id:
        return jsonify({"success": False, "error": "No active session"}), 403

    session_data = get_session_by_id(db, session_id)
    if not session_data or session_data["created_by"] != ObjectId(session["userId"]):
        return jsonify({"success": False, "error": "Not the session master"}), 403

    remove_character_from_session(db, session_id, char_id)
    socketio.emit("session_sync", build_session_snapshot(db, session_id), room=session_id)

    return jsonify({"success": True})


# ---------------------------------------------------------------------------
# Gameplay APIs
# ---------------------------------------------------------------------------

@app.route("/use_skill", methods=["POST"])
def use_skill():
    data = request.get_json(force=True, silent=True) or {}
    char_id = data.get("char_id")
    cost = data.get("cost") or {}

    character = get_character_by_id(db, char_id)
    if not character:
        return jsonify({"success": False, "message": "Character not found"}), 404

    resources = character.get("resources", {})
    for resource_key, amount in cost.items():
        if resources.get(resource_key, {}).get("current", 0) < amount:
            return jsonify({"success": False, "message": "Recursos insuficientes"}), 400

    update_fields = {}
    for resource_key, amount in cost.items():
        new_value = resources[resource_key]["current"] - amount
        resources[resource_key]["current"] = new_value
        update_fields[f"resources.{resource_key}.current"] = new_value

    if update_fields:
        db.chars.update_one({"_id": ObjectId(char_id)}, {"$set": update_fields})

    session_id = db.sessions.find_one({"characters": ObjectId(char_id)})
    if session_id:
        socketio.emit("resources_updated", {
            "character_id": str(character["_id"]),
            "resources": resources,
        }, room=str(session_id["_id"]))

    return jsonify({"success": True, "resources": resources})


def _character_details_payload(character):
    class_info = get_class_by_id(db, character["class_id"]) if character.get("class_id") else None
    race_info = get_race_by_id(db, character["race_id"]) if character.get("race_id") else None

    habilidades = []
    for habilidade_id, habilidade_data in character.get("habilidades", {}).items():
        habilidades.append({
            "id": habilidade_id,
            "name": habilidade_data.get("name"),
            "description": habilidade_data.get("description"),
            "cost": habilidade_data.get("cost", {}),
        })

    return {
        "name": character["name"],
        "system_id": character["system_id"],
        "class_name": class_info["name"] if class_info else "Desconhecido",
        "race_name": race_info["name"] if race_info else None,
        "attributes": character.get("attributes", {}),
        "resources": character.get("resources", {}),
        "combat_stats": character.get("combat_stats", {}),
        "habilidades": habilidades,
        "pericias": character.get("pericias", {}),
        "img_url": character.get("img_url") or "/static/images/default.png",
    }


@app.route("/get_player_details/<player_id>", methods=["GET"])
def get_player_details(player_id):
    character = get_character_by_id(db, player_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(_character_details_payload(character))


@app.route("/get_current_player_details", methods=["GET"])
def get_current_player_details():
    character_id = session.get("character_id")
    character = get_character_by_id(db, character_id) if character_id else None
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(_character_details_payload(character))


# ---------------------------------------------------------------------------
# Media / music (scoped to the requesting session's room)
# ---------------------------------------------------------------------------

@app.route("/upload_media", methods=["POST"])
def upload_media():
    if "media" not in request.files:
        return jsonify({"error": "No media file provided"}), 400

    file = request.files["media"]
    session_id = request.form.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    display_time = request.form.get("display_time", type=int)

    if not allowed_file(file.filename, ALLOWED_MEDIA_EXTENSIONS):
        return jsonify({"error": "File not allowed"}), 400

    file_path = save_upload(file, app.config["MEDIA_FOLDER"])
    media_url = "/" + file_path.replace(os.sep, "/")

    socketio.emit("new_media", {"media_url": media_url, "display_time": display_time}, room=session_id)
    return jsonify({"success": True, "media_url": media_url})


@app.route("/music_tracks", methods=["GET"])
def get_music_tracks():
    tracks = []
    for filename in sorted(os.listdir(app.config["MUSIC_FOLDER"])):
        if filename.lower().endswith(("mp3", "wav", "ogg")):
            tracks.append({
                "name": filename.rsplit(".", 1)[0],
                "url": url_for("static", filename=f"music/{filename}"),
            })
    return jsonify(tracks)


@app.route("/play_music", methods=["POST"])
def play_music():
    data = request.get_json(force=True, silent=True) or {}
    track_url = data.get("track_url")
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"error": "session_id is required"}), 400
    if not track_url:
        return jsonify({"error": "No track URL provided"}), 400

    relative_path = track_url.replace("/static/", "", 1)
    if not os.path.exists(os.path.join(app.static_folder, relative_path)):
        return jsonify({"error": "Track not found"}), 404

    socketio.emit("play_music", {"track_url": track_url}, room=session_id)
    return jsonify({"success": True})


@app.route("/stop_music", methods=["POST"])
def stop_music():
    data = request.get_json(force=True, silent=True) or {}
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    socketio.emit("stop_music", {}, room=session_id)
    return jsonify({"success": True})


# ---------------------------------------------------------------------------
# PDF export
# ---------------------------------------------------------------------------

pdfmetrics.registerFont(TTFont("MedievalFont", "static/fonts/Enchanted Land.otf"))


@app.route("/export_pdf/<character_id>")
def export_pdf(character_id):
    character = get_character_by_id(db, character_id)
    if not character:
        return "Character not found", 404

    system = get_system(character["system_id"])
    class_info = get_class_by_id(db, character["class_id"]) if character.get("class_id") else None
    race_info = get_race_by_id(db, character["race_id"]) if character.get("race_id") else None

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFillColorRGB(0.96, 0.87, 0.70)
    p.rect(0, 0, width, height, stroke=0, fill=1)

    p.setFont("MedievalFont", 24)
    p.setFillColor(colors.darkred)
    p.drawCentredString(width / 2.0, height - 50, f"Ficha de Personagem: {character['name']}")

    if character.get("img_url"):
        image_path = character["img_url"].lstrip("/")
        extension = os.path.splitext(image_path)[1].lower()
        try:
            if extension in [".png", ".jpg", ".jpeg", ".webp"] and os.path.exists(image_path):
                img_x, img_y, img_size = width - 220, height - 250, 150
                p.setStrokeColor(colors.black)
                p.setLineWidth(2)
                p.rect(img_x - 10, img_y - 10, img_size + 20, img_size + 20)
                p.drawImage(ImageReader(image_path), img_x, img_y, width=img_size, height=img_size)
        except Exception as e:
            logging.warning("Could not embed character image in PDF: %s", e)

    text_x = 60
    y = height - 150
    line_height = 20

    def line(label, value):
        nonlocal y
        p.setFillColor(colors.darkred)
        p.drawString(text_x, y, f"{label}:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 140, y, str(value))
        y -= line_height

    p.setFont("MedievalFont", 16)
    line(system["class_label"], class_info["name"] if class_info else "Desconhecido")
    if system["uses_race"]:
        line(system["race_label"], race_info["name"] if race_info else "Desconhecido")
    for res in system["resources"]:
        line(res["label"], character.get("resources", {}).get(res["key"], {}).get("max", 0))
    for attr in system["attributes"]:
        line(attr["label"], character.get("attributes", {}).get(attr["key"], 0))

    y -= line_height
    p.setFont("MedievalFont", 18)
    p.setFillColor(colors.darkred)
    p.drawString(text_x, y, system["ability_label"] + ":")
    y -= line_height
    p.setFont("MedievalFont", 14)
    for _, habilidade in character.get("habilidades", {}).items():
        p.setFillColor(colors.black)
        p.drawString(text_x + 20, y, f"{habilidade['name']}: {habilidade['description']}")
        y -= line_height

    y -= line_height
    p.setFont("MedievalFont", 18)
    p.setFillColor(colors.darkred)
    p.drawString(text_x, y, system["skill_label"] + ":")
    y -= line_height
    p.setFont("MedievalFont", 14)
    for pericia, valor in character.get("pericias", {}).items():
        p.setFillColor(colors.black)
        p.drawString(text_x + 20, y, f"{pericia}: +{valor}")
        y -= line_height

    if character.get("origem"):
        y -= line_height
        p.setFont("MedievalFont", 18)
        p.setFillColor(colors.darkred)
        p.drawString(text_x, y, system["history_label"] + ":")
        y -= line_height
        p.setFont("MedievalFont", 14)
        for text_line in character["origem"].split("\n"):
            p.setFillColor(colors.black)
            p.drawString(text_x + 20, y, text_line)
            y -= line_height

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{character['name']}_Ficha.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    socketio.run(
        app,
        debug=Config.DEBUG,
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 8000)),
    )
