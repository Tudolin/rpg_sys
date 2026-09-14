from local_db import ObjectId

from game_systems import get_system
from models.class_model import get_class_by_id
from models.race_model import get_race_by_id


def _compute_attributes(system, base_attributes, selected_race):
    attributes = {}
    for attr in system["attributes"]:
        value = int(base_attributes.get(attr["key"], 0))
        if selected_race:
            value += selected_race.get("attribute_bonuses", {}).get(attr["key"], 0)
        attributes[attr["key"]] = value
    return attributes


def _compute_resources(system, attributes, selected_class):
    resource_bases = (selected_class or {}).get("resource_bases", {})
    resources = {}
    for res in system["resources"]:
        base = resource_bases.get(res["key"], 0)
        governing = res.get("governing_attribute")
        bonus = attributes.get(governing, 0) if governing else 0
        max_value = max(base + bonus, 1)
        resources[res["key"]] = {"max": max_value, "current": max_value}
    return resources


def _compute_combat_stats(system, attributes, selected_class):
    combat_bases = (selected_class or {}).get("combat_bases", {})
    stats = {}
    for stat in system.get("combat_stats", []):
        base = combat_bases.get(stat["key"], 0)
        governing = stat.get("governing_attribute")
        bonus = attributes.get(governing, 0) if governing else 0
        stats[stat["key"]] = base + bonus
    return stats


def create_character(db, user_id, system_id, name, class_id, race_id, img_url,
                      base_attributes, origem, pericias_selecionadas, habilidades_selecionadas):
    system = get_system(system_id)

    selected_class = get_class_by_id(db, class_id) if class_id else None
    selected_race = get_race_by_id(db, race_id) if (system["uses_race"] and race_id) else None

    attributes = _compute_attributes(system, base_attributes, selected_race)
    resources = _compute_resources(system, attributes, selected_class)
    combat_stats = _compute_combat_stats(system, attributes, selected_class)

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

    pericias = {pericia: 4 for pericia in pericias_selecionadas}

    character = {
        "user_id": ObjectId(user_id),
        "system_id": system_id,
        "name": name,
        "class_id": ObjectId(class_id) if class_id else None,
        "race_id": ObjectId(race_id) if race_id else None,
        "img_url": img_url,
        "attributes": attributes,
        "resources": resources,
        "combat_stats": combat_stats,
        "habilidades": habilidades,
        "pericias": pericias,
        "origem": origem,
    }

    result = db.chars.insert_one(character)
    character["_id"] = result.inserted_id
    return character


# --- Legacy compatibility -------------------------------------------------
# Characters created by the previous version of this app store attributes
# and resources as flat top-level fields (forca, hp, current_hp, ...)
# instead of the generic `attributes` / `resources` dicts used now. Rather
# than requiring a hard cutover, every read normalizes on the fly so old
# characters keep working. `migrate_legacy_characters.py` persists this
# shape for anyone who wants a one-time, permanent migration.
_LEGACY_ATTRIBUTE_KEYS = ["forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma"]
_LEGACY_RESOURCE_KEYS = {"hp": "hp", "mana": "mana", "energia": "energia"}


def normalize_character(character):
    if character is None:
        return None

    character.setdefault("system_id", "medieval")

    if "attributes" not in character:
        character["attributes"] = {
            key: character.get(key, 0) for key in _LEGACY_ATTRIBUTE_KEYS if key in character
        }

    if "resources" not in character:
        resources = {}
        for key, legacy_key in _LEGACY_RESOURCE_KEYS.items():
            if legacy_key in character:
                max_value = character.get(legacy_key, 0)
                current_value = character.get(f"current_{legacy_key}" if legacy_key != "energia" else "current_energy", max_value)
                resources[key] = {"max": max_value, "current": current_value}
        character["resources"] = resources

    character.setdefault("combat_stats", {
        key: character[key] for key in ("ataque", "defesa") if key in character
    })

    return character


def delete_character(db, character_id):
    db.chars.delete_one({"_id": ObjectId(character_id)})


def update_character(db, character_id, name, class_id, race_id, img_url, origem):
    db.chars.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": {
            "name": name,
            "class_id": ObjectId(class_id),
            "race_id": ObjectId(race_id) if race_id else None,
            "img_url": img_url,
            "origem": origem,
        }}
    )


def get_character_by_id(db, character_id):
    return normalize_character(db.chars.find_one({"_id": ObjectId(character_id)}))


def get_character_by_user(db, user_id):
    return normalize_character(db.chars.find_one({"user_id": ObjectId(user_id)}))


def get_characters_by_user(db, user_id):
    characters = db.chars.find({"user_id": ObjectId(user_id)})
    enriched_characters = []

    for char in characters:
        normalize_character(char)
        char_class = get_class_by_id(db, char["class_id"]) if char.get("class_id") else None
        char_race = get_race_by_id(db, char["race_id"]) if char.get("race_id") else None

        char["class_name"] = char_class["name"] if char_class else "Desconhecido"
        char["race_name"] = char_race["name"] if char_race else None
        enriched_characters.append(char)

    return enriched_characters
