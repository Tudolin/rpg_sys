from bson import ObjectId


def create_default_classes(db):
    classes = [
        {
            "name": "Guerreiro",
            "hp": 20,
            "forca": 20,
            "destreza": 5,
            "defense": 5,
            "pericias": {
                "Luta": "Força",
                "Pontaria": "Destreza",
                "Fortitude": "Constituição",
                "Atletismo": "Força",
                "Cavalgar": "Destreza",
                "Guerra": "Inteligência",
                "Ofício": "Inteligência",
                "Percepção": "Sabedoria",
                "Reflexos": "Destreza"
            },
            "habilidades_classe": {
                "Ataque Preciso": "Aumenta a precisão dos ataques",
                "Resistência a Dano": "Reduz o dano recebido em combate",
                "Maestria em Armas": "Aumenta a eficácia das armas utilizadas"
            }
        },
        {
            "name": "Mago",
            "hp": 8,
            "forca": 5,
            "destreza": 10,
            "defense": 2,
            "pericias": {
                "Magia": "Inteligência",
                "Alquimia": "Inteligência",
                "Conhecimento": "Inteligência",
                "Ofício": "Inteligência",
                "Linguística": "Inteligência",
                "Percepção": "Sabedoria",
                "Reflexos": "Destreza"
            },
            "habilidades_classe": {
                "Magia Arcana": "Permite lançar feitiços e manipular energia mágica",
                "Conhecimento Mágico": "Aumenta o entendimento e o uso de magia",
                "Mana Aprimorado": "Aumenta a quantidade de mana disponível"
            }
        }
        # Adicione mais classes conforme necessário
    ]
    db.classes.insert_many(classes)


def get_class_by_id(db, class_id):
    return db.classes.find_one({"_id": ObjectId(class_id)})
