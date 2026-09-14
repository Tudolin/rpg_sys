"""Password hashing helpers.

Existing accounts (created by the previous version of this app) store
passwords in plain text. `verify_password` accepts both a modern hash and
a legacy plain-text value so nobody gets locked out; `needs_upgrade` tells
the caller when it should re-save the hash after a successful login.
"""
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(raw_password):
    return generate_password_hash(raw_password)


def _looks_hashed(stored_password):
    return isinstance(stored_password, str) and "$" in stored_password and (
        stored_password.startswith("pbkdf2:")
        or stored_password.startswith("scrypt:")
        or stored_password.startswith("argon2")
    )


def verify_password(stored_password, provided_password):
    if not stored_password:
        return False
    if _looks_hashed(stored_password):
        return check_password_hash(stored_password, provided_password)
    # Legacy plain-text account.
    return stored_password == provided_password


def needs_upgrade(stored_password):
    return not _looks_hashed(stored_password)
