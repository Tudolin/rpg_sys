"""Serialização de personagem compartilhada pela API REST e pelo Socket.IO.

Ambos os canais entregam a ficha no mesmo formato, então o frontend pode
renderizar um personagem vindo de `GET /api/characters` ou de um
`session_sync` sem tratar dois formatos diferentes.
"""
from game_systems import DEFAULT_SYSTEM_ID
from models.class_model import get_class_by_id
from models.race_model import get_race_by_id


def ability_list(character):
    """Habilidades sempre como lista, independente de como foram gravadas."""
    return [
        {
            "id": ability_id,
            "name": data.get("name"),
            "description": data.get("description", ""),
            "cost": data.get("cost", {}),
            "icon": data.get("icon"),
        }
        for ability_id, data in (character.get("habilidades") or {}).items()
    ]


def serialize_character(db, character):
    class_info = get_class_by_id(db, character["class_id"]) if character.get("class_id") else None
    race_info = get_race_by_id(db, character["race_id"]) if character.get("race_id") else None

    return {
        "_id": str(character["_id"]),
        "name": character["name"],
        "system_id": character.get("system_id", DEFAULT_SYSTEM_ID),
        "class_id": str(character["class_id"]) if character.get("class_id") else None,
        "race_id": str(character["race_id"]) if character.get("race_id") else None,
        "class_name": class_info["name"] if class_info else "Desconhecido",
        "race_name": race_info["name"] if race_info else None,
        "img_url": character.get("img_url") or "/static/images/default.png",
        "attributes": character.get("attributes", {}),
        "resources": character.get("resources", {}),
        "combat_stats": character.get("combat_stats", {}),
        "habilidades": ability_list(character),
        "pericias": character.get("pericias", {}),
        "origem": character.get("origem", ""),
    }


def serialize_monster(monster):
    monster = dict(monster)
    monster["current_hp"] = monster.get("current_hp", monster.get("hp", 0))
    monster["current_mana"] = monster.get("current_mana", monster.get("mana", 0))
    monster["current_energia"] = monster.get("current_energia", monster.get("energia", 0))
    return monster
