from local_db import ObjectId

from game_systems import DEFAULT_SYSTEM_ID


def create_session(db, session_name, user_id, system_id=DEFAULT_SYSTEM_ID):
    session_data = {
        "name": session_name,
        "created_by": ObjectId(user_id),
        "system_id": system_id,
        "characters": [],
        "monsters": [],
    }
    result = db.sessions.insert_one(session_data)
    return result.inserted_id

def get_all_sessions(db):
    return db.sessions.find()

def get_session_by_id(db, session_id):
    session_data = db.sessions.find_one({"_id": ObjectId(session_id)})
    if session_data is not None:
        session_data.setdefault("system_id", DEFAULT_SYSTEM_ID)
        session_data.setdefault("monsters", [])
        session_data.setdefault("characters", [])
    return session_data

def add_character_to_session(db, session_id, character_id):
    db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$push": {"characters": ObjectId(character_id)}}
    )

def remove_character_from_session(db, session_id, character_id):
    db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$pull": {"characters": ObjectId(character_id)}}
    )
