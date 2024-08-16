from bson import ObjectId

from models.class_model import get_class_by_id
from models.race_model import get_race_by_id


def get_class_by_id(db, class_id):
    return db['classes.classes'].find_one({"_id": ObjectId(class_id)})

def get_race_by_id(db, race_id):
    return db['races.races'].find_one({"_id": ObjectId(race_id)})

def get_class_by_id(db, class_id):
    return db['classes.classes'].find_one({"_id": ObjectId(class_id)})

def get_race_by_id(db, race_id):
    return db['races.races'].find_one({"_id": ObjectId(race_id)})

def create_character(db, user_id, name, class_id, race_id, img_url, forca, destreza, constituicao, inteligencia, sabedoria, carisma, origem, pericias_selecionadas):
    selected_class = get_class_by_id(db, class_id)
    selected_race = get_race_by_id(db, race_id)

    # Aplique os bônus da raça aos atributos
    forca += selected_race.get('forca_bonus', 0)
    destreza += selected_race.get('destreza_bonus', 0)
    constituicao += selected_race.get('constituicao_bonus', 0)
    inteligencia += selected_race.get('inteligencia_bonus', 0)
    sabedoria += selected_race.get('sabedoria_bonus', 0)
    carisma += selected_race.get('carisma_bonus', 0)

    # Calcula HP e outras características baseadas em atributos e classe
    hp = selected_class['hp'] + constituicao
    ataque = selected_class['forca'] + forca
    defesa = selected_class['defense'] + destreza

    # Adiciona as habilidades herdadas da classe e da raça
    habilidades = {}

    # Adiciona habilidades da classe
    for habilidade, descricao in selected_class.get('habilidades_classe', {}).items():
        habilidades[habilidade] = descricao

    # Adiciona habilidades da raça
    for habilidade, descricao in selected_race.get('habilidades_inatas', {}).items():
        habilidades[habilidade] = descricao

    # Processa as perícias selecionadas
    pericias = {}
    for pericia in pericias_selecionadas:
        pericias[pericia] = 4  # Adiciona +4 ao atributo de cada perícia selecionada

    # Adiciona perícias herdadas da classe
    if 'pericias_classe' in selected_class:
        for pericia, valor in selected_class['pericias_classe'].items():
            pericias[pericia] = valor

    # Adiciona perícias herdadas da raça
    if 'pericias_raca' in selected_race:
        for pericia, valor in selected_race['pericias_raca'].items():
            pericias[pericia] = valor

    character = {
        "user_id": ObjectId(user_id),
        "name": name,
        "class_id": ObjectId(class_id),
        "race_id": ObjectId(race_id),
        "img_url": img_url,
        "forca": forca,
        "destreza": destreza,
        "constituicao": constituicao,
        "inteligencia": inteligencia,
        "sabedoria": sabedoria,
        "carisma": carisma,
        "hp": hp,
        "ataque": ataque,
        "defesa": defesa,
        "habilidades": habilidades,
        "pericias": pericias,
        "origem": origem
    }

    db.chars.insert_one(character)



def delete_character(db, character_id):
    db.chars.delete_one({"_id": ObjectId(character_id)})

def update_character(db, character_id, name, class_id, race_id, img_url, origem):
    db.chars.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": {
            "name": name,
            "class_id": ObjectId(class_id),
            "race_id": ObjectId(race_id),
            "img_url": img_url,
            "origem": origem
        }}
    )

def get_characters_by_user(db, user_id):
    characters = db.chars.find({"user_id": ObjectId(user_id)})
    enriched_characters = []

    for char in characters:
        char_class = get_class_by_id(db, char['class_id'])
        char_race = get_race_by_id(db, char['race_id'])

        char['class_name'] = char_class['name'] if char_class else "Classe Desconhecida"
        char['race_name'] = char_race['name'] if char_race else "Raça Desconhecida"
        enriched_characters.append(char)

    return enriched_characters



