from local_db import ObjectId

from security import hash_password, needs_upgrade, verify_password


def get_user_by_username(db, username):
    return db.users.find_one({"username": username})


def get_user_by_id(db, user_id):
    return db.users.find_one({"_id": ObjectId(user_id)})


def create_user(db, username, password):
    """Create a new user. Returns the new user id, or None if the username is taken."""
    if get_user_by_username(db, username):
        return None
    result = db.users.insert_one({
        "username": username,
        "password": hash_password(password),
    })
    return str(result.inserted_id)


def verify_credentials(db, username, password):
    """Check a login attempt. Returns the user document on success, else None.

    Transparently upgrades legacy plain-text passwords to a hash on
    successful login, so existing accounts keep working.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(user.get("password"), password):
        return None

    if needs_upgrade(user.get("password")):
        db.users.update_one({"_id": user["_id"]}, {"$set": {"password": hash_password(password)}})

    return user
