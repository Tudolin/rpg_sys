"""A tiny local, file-based document store, standing in for MongoDB.

This app used to require a MongoDB server (originally a hardcoded Atlas
cloud cluster). For a fully self-hosted, single-Debian-box deployment
that's one more moving part than a small friends'-table game needs, so
every "collection" here is just a SQLite table of `(id, json blob)` rows,
speaking the same small slice of the pymongo API the rest of the app
already uses: `find_one`, `find`, `insert_one`, `update_one` (`$set`,
`$push`, `$pull`), `delete_one`, plus an `ObjectId` compatible enough
(string-backed, equality/str/repr) that every existing `ObjectId(...)`
call site in models/app.py/sockets.py keeps working untouched.

Not a general Mongo clone: only the filter/update shapes this codebase
actually issues are supported (see the model files for what those are).
"""
import copy
import json
import threading
import uuid

_lock = threading.Lock()


class ObjectId:
    """A minimal stand-in for bson.ObjectId: an opaque, stringly-typed id."""

    __slots__ = ("_hex",)

    def __init__(self, value=None):
        if value is None:
            self._hex = uuid.uuid4().hex
        elif isinstance(value, ObjectId):
            self._hex = value._hex
        elif isinstance(value, str):
            if not value:
                raise ValueError("ObjectId string cannot be empty")
            self._hex = value
        else:
            raise TypeError(f"Cannot build ObjectId from {type(value)!r}")

    def __str__(self):
        return self._hex

    def __repr__(self):
        return f"ObjectId('{self._hex}')"

    def __eq__(self, other):
        if isinstance(other, ObjectId):
            return self._hex == other._hex
        if isinstance(other, str):
            return self._hex == other
        return NotImplemented

    def __hash__(self):
        return hash(self._hex)


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return {"$oid": str(obj)}
        return super().default(obj)


def _decode(obj):
    if isinstance(obj, dict):
        if set(obj.keys()) == {"$oid"}:
            return ObjectId(obj["$oid"])
        return {key: _decode(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_decode(item) for item in obj]
    return obj


def _dumps(doc):
    return json.dumps(doc, cls=_JSONEncoder)


def _loads(raw):
    return _decode(json.loads(raw))


def _values_equal(a, b):
    if isinstance(a, ObjectId) or isinstance(b, ObjectId):
        return str(a) == str(b)
    return a == b


def _matches(doc, filter_):
    for key, expected in filter_.items():
        actual = doc.get(key)
        if isinstance(expected, dict) and "$in" in expected:
            if not any(_values_equal(actual, candidate) for candidate in expected["$in"]):
                return False
            continue
        if isinstance(actual, list):
            # Mongo semantics: a scalar filter value matches if it is a
            # member of the stored array (e.g. {"characters": ObjectId(x)}).
            if isinstance(expected, dict):
                # A dict filter against a list of dicts: match if any
                # element satisfies every key (used by monster removal).
                if not any(_matches(item, expected) for item in actual if isinstance(item, dict)):
                    return False
            elif not any(_values_equal(item, expected) for item in actual):
                return False
        else:
            if not _values_equal(actual, expected):
                return False
    return True


def _get_path(doc, dotted_key):
    node = doc
    for part in dotted_key.split("."):
        if not isinstance(node, dict):
            return None
        node = node.get(part)
    return node


def _set_path(doc, dotted_key, value):
    parts = dotted_key.split(".")
    node = doc
    for part in parts[:-1]:
        if part not in node or not isinstance(node[part], dict):
            node[part] = {}
        node = node[part]
    node[parts[-1]] = value


def _apply_update(doc, update):
    doc = copy.deepcopy(doc)
    for op, changes in update.items():
        if op == "$set":
            for key, value in changes.items():
                _set_path(doc, key, value)
        elif op == "$push":
            for key, value in changes.items():
                current = _get_path(doc, key)
                if not isinstance(current, list):
                    current = []
                current.append(value)
                _set_path(doc, key, current)
        elif op == "$pull":
            for key, condition in changes.items():
                current = _get_path(doc, key)
                if not isinstance(current, list):
                    continue
                if isinstance(condition, dict):
                    remaining = [item for item in current if not (isinstance(item, dict) and _matches(item, condition))]
                else:
                    remaining = [item for item in current if not _values_equal(item, condition)]
                _set_path(doc, key, remaining)
        else:
            raise NotImplementedError(f"Unsupported update operator: {op}")
    return doc


class _InsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class Collection:
    def __init__(self, conn, name):
        self._conn = conn
        self._name = name
        with _lock:
            self._conn.execute(
                f'CREATE TABLE IF NOT EXISTS "{self._name}" (id TEXT PRIMARY KEY, data TEXT NOT NULL)'
            )
            self._conn.commit()

    def _all_docs(self):
        rows = self._conn.execute(f'SELECT data FROM "{self._name}"').fetchall()
        return [_loads(row[0]) for row in rows]

    def find_one(self, filter_=None):
        filter_ = filter_ or {}
        if "_id" in filter_ and not isinstance(filter_["_id"], dict):
            row = self._conn.execute(
                f'SELECT data FROM "{self._name}" WHERE id = ?', (str(filter_["_id"]),)
            ).fetchone()
            if row is None:
                return None
            doc = _loads(row[0])
            return doc if _matches(doc, filter_) else None

        with _lock:
            for doc in self._all_docs():
                if _matches(doc, filter_):
                    return doc
        return None

    def find(self, filter_=None):
        filter_ = filter_ or {}
        with _lock:
            return [doc for doc in self._all_docs() if _matches(doc, filter_)]

    def insert_one(self, doc):
        doc = copy.deepcopy(doc)
        if "_id" not in doc or doc["_id"] is None:
            doc["_id"] = ObjectId()
        with _lock:
            self._conn.execute(
                f'INSERT INTO "{self._name}" (id, data) VALUES (?, ?)',
                (str(doc["_id"]), _dumps(doc)),
            )
            self._conn.commit()
        return _InsertResult(doc["_id"])

    def update_one(self, filter_, update, upsert=False):
        with _lock:
            target = None
            for doc in self._all_docs():
                if _matches(doc, filter_):
                    target = doc
                    break

            if target is None:
                if not upsert:
                    return None
                base = {"_id": filter_.get("_id", ObjectId())}
                for key, value in filter_.items():
                    if key != "_id" and not isinstance(value, dict):
                        base[key] = value
                new_doc = _apply_update(base, update)
                self._conn.execute(
                    f'INSERT INTO "{self._name}" (id, data) VALUES (?, ?)',
                    (str(new_doc["_id"]), _dumps(new_doc)),
                )
                self._conn.commit()
                return _InsertResult(new_doc["_id"])

            updated = _apply_update(target, update)
            self._conn.execute(
                f'UPDATE "{self._name}" SET data = ? WHERE id = ?',
                (_dumps(updated), str(target["_id"])),
            )
            self._conn.commit()
        return None

    def delete_one(self, filter_):
        with _lock:
            for doc in self._all_docs():
                if _matches(doc, filter_):
                    self._conn.execute(f'DELETE FROM "{self._name}" WHERE id = ?', (str(doc["_id"]),))
                    self._conn.commit()
                    return
