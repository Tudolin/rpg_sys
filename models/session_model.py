from bson import ObjectId


def create_session(db, session_name, user_id):
    session_data = {
        "name": session_name,
        "created_by": ObjectId(user_id),
        "characters": []
    }
    result = db.sessions.insert_one(session_data)
    return result.inserted_id

def get_all_sessions(db):
    return db.sessions.find()

def get_session_by_id(db, session_id):
    return db.sessions.find_one({"_id": ObjectId(session_id)})

def add_character_to_session(db, session_id, character_id):
    db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$push": {"characters": ObjectId(character_id)}}
    )

def remove_character_from_session(db, session_id, character_id):
    session_data = db.sessions.find_one({"_id": ObjectId(session_id)})
    if session_data:
        updated_characters = [char for char in session_data.get('characters', []) if char != ObjectId(character_id)]
        db.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"characters": updated_characters}}
        )


def remove_character_from_session(db, session_id, character_id):
    db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$pull": {"characters": ObjectId(character_id)}}
    )
