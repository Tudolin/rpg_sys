"""Registry of supported RPG systems (rulesets).

The app used to hardcode D&D/Tormenta-style medieval fantasy everywhere
(Força/Destreza/.../Mana/Energia, "Classe", "Raça", ...). This module turns
that into one entry in a registry, so a table can instead play Call of
Cthulhu, a Western, or Cyberpunk with a character sheet, resource orbs and
terminology that actually fit the genre.

A system definition is intentionally data-only (no code) so templates and
JS can render a sheet generically: loop over `attributes` and `resources`
instead of hardcoding field names.
"""

DEFAULT_SYSTEM_ID = "medieval"


def _attr(key, label, abbr=None):
    return {"key": key, "label": label, "abbr": abbr or label[:3].upper()}


def _resource(key, label, color, governing_attribute=None):
    return {"key": key, "label": label, "color": color, "governing_attribute": governing_attribute}


def _combat_stat(key, label, governing_attribute=None):
    return {"key": key, "label": label, "governing_attribute": governing_attribute}


SYSTEMS = {
    "medieval": {
        "id": "medieval",
        "name": "Fantasia Medieval",
        "tagline": "Espadas, magia e dragões — no estilo D&D / Tormenta.",
        "icon": "🗡️",
        "theme": "medieval",
        "uses_class": True,
        "class_label": "Classe",
        "uses_race": True,
        "race_label": "Raça",
        "attributes": [
            _attr("forca", "Força"),
            _attr("destreza", "Destreza"),
            _attr("constituicao", "Constituição"),
            _attr("inteligencia", "Inteligência"),
            _attr("sabedoria", "Sabedoria"),
            _attr("carisma", "Carisma"),
        ],
        "resources": [
            _resource("hp", "Vida", "red", governing_attribute="constituicao"),
            _resource("mana", "Mana", "blue", governing_attribute="inteligencia"),
            _resource("energia", "Energia", "yellow", governing_attribute="destreza"),
        ],
        "combat_stats": [
            _combat_stat("ataque", "Ataque", governing_attribute="forca"),
            _combat_stat("defesa", "Defesa", governing_attribute="destreza"),
        ],
        "skill_label": "Perícias",
        "ability_label": "Habilidades",
        "history_label": "História do Personagem",
    },
    "cthulhu": {
        "id": "cthulhu",
        "name": "Horror Investigativo",
        "tagline": "Segredos que a mente humana não deveria conhecer.",
        "icon": "🐙",
        "theme": "cthulhu",
        "uses_class": True,
        "class_label": "Ocupação",
        "uses_race": False,
        "race_label": None,
        "attributes": [
            _attr("forca", "Força"),
            _attr("destreza", "Destreza"),
            _attr("constituicao", "Constituição"),
            _attr("inteligencia", "Inteligência"),
            _attr("educacao", "Educação"),
            _attr("poder", "Poder"),
        ],
        "resources": [
            _resource("hp", "Vida", "red", governing_attribute="constituicao"),
            _resource("sanidade", "Sanidade", "purple", governing_attribute="poder"),
            _resource("sorte", "Sorte", "yellow", governing_attribute="poder"),
        ],
        "combat_stats": [],
        "skill_label": "Perícias",
        "ability_label": "Talentos",
        "history_label": "Histórico do Investigador",
    },
    "western": {
        "id": "western",
        "name": "Velho Oeste",
        "tagline": "Pó, pólvora e pistoleiros numa terra sem lei.",
        "icon": "🤠",
        "theme": "western",
        "uses_class": True,
        "class_label": "Arquétipo",
        "uses_race": False,
        "race_label": None,
        "attributes": [
            _attr("forca", "Força"),
            _attr("destreza", "Destreza"),
            _attr("constituicao", "Constituição"),
            _attr("sagacidade", "Sagacidade"),
            _attr("carisma", "Carisma"),
        ],
        "resources": [
            _resource("hp", "Vida", "red", governing_attribute="constituicao"),
            _resource("determinacao", "Determinação", "yellow", governing_attribute="carisma"),
        ],
        "combat_stats": [
            _combat_stat("pontaria", "Pontaria", governing_attribute="destreza"),
        ],
        "skill_label": "Perícias",
        "ability_label": "Talentos",
        "history_label": "Passado do Pistoleiro",
    },
    "cyberpunk": {
        "id": "cyberpunk",
        "name": "Cyberpunk",
        "tagline": "Neon, implantes e corporações numa metrópole sombria.",
        "icon": "🤖",
        "theme": "cyberpunk",
        "uses_class": True,
        "class_label": "Papel",
        "uses_race": False,
        "race_label": None,
        "attributes": [
            _attr("forca", "Força"),
            _attr("reflexos", "Reflexos"),
            _attr("tecnica", "Técnica"),
            _attr("inteligencia", "Inteligência"),
            _attr("vontade", "Vontade"),
            _attr("frieza", "Frieza"),
        ],
        "resources": [
            _resource("hp", "Vida", "red", governing_attribute="vontade"),
            _resource("humanidade", "Humanidade", "purple", governing_attribute="vontade"),
            _resource("energia", "Energia Cibernética", "blue", governing_attribute="tecnica"),
        ],
        "combat_stats": [
            _combat_stat("ataque", "Ataque", governing_attribute="reflexos"),
        ],
        "skill_label": "Perícias",
        "ability_label": "Implantes & Talentos",
        "history_label": "Dossiê do Personagem",
    },
}


def get_system(system_id):
    return SYSTEMS.get(system_id, SYSTEMS[DEFAULT_SYSTEM_ID])


def system_choices():
    """List of systems for a <select>, in a stable, deliberate order."""
    order = ["medieval", "cthulhu", "western", "cyberpunk"]
    return [SYSTEMS[key] for key in order if key in SYSTEMS]


def attribute_keys(system_id):
    return [a["key"] for a in get_system(system_id)["attributes"]]


def resource_keys(system_id):
    return [r["key"] for r in get_system(system_id)["resources"]]
