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
    },
    {
        "name": "Ladino",
        "hp": 12,
        "forca": 10,
        "destreza": 15,
        "defense": 3,
        "pericias": {
            "Furtividade": "Destreza",
            "Crime": "Destreza",
            "Enganação": "Carisma",
            "Percepção": "Sabedoria",
            "Acrobacia": "Destreza",
            "Reflexos": "Destreza",
            "Diplomacia": "Carisma",
            "Luta": "Força",
            "Pontaria": "Destreza"
        },
        "habilidades_classe": {
            "Ataque Furtivo": "Dano extra ao atacar inimigos desatentos",
            "Evasão": "Reduz o dano de ataques em área",
            "Desarmar Armadilhas": "Permite desarmar armadilhas e mecanismos"
        }
    },
    {
        "name": "Clérigo",
        "hp": 16,
        "forca": 10,
        "destreza": 8,
        "defense": 4,
        "pericias": {
            "Religião": "Sabedoria",
            "Magia": "Sabedoria",
            "Cura": "Sabedoria",
            "Conhecimento": "Inteligência",
            "Intimidação": "Carisma",
            "Percepção": "Sabedoria",
            "Ofício": "Inteligência",
            "Fortitude": "Constituição"
        },
        "habilidades_classe": {
            "Canalizar Energia": "Recupera pontos de vida ou causa dano a mortos-vivos",
            "Milagre": "Permite lançar feitiços divinos poderosos",
            "Abençoar": "Aumenta as habilidades de aliados temporariamente"
        }
    },
    {
        "name": "Paladino",
        "hp": 18,
        "forca": 15,
        "destreza": 8,
        "defense": 6,
        "pericias": {
            "Luta": "Força",
            "Fortitude": "Constituição",
            "Religião": "Sabedoria",
            "Cavalgar": "Destreza",
            "Cura": "Sabedoria",
            "Intimidação": "Carisma",
            "Percepção": "Sabedoria",
            "Reflexos": "Destreza"
        },
        "habilidades_classe": {
            "Imposição das Mãos": "Cura a si mesmo ou a outros com um toque",
            "Aura de Coragem": "Imunidade ao medo e bônus para aliados próximos",
            "Golpe Divino": "Causa dano extra contra criaturas malignas"
        }
    },
    {
        "name": "Bardo",
        "hp": 14,
        "forca": 8,
        "destreza": 12,
        "defense": 3,
        "pericias": {
            "Atuação": "Carisma",
            "Enganação": "Carisma",
            "Diplomacia": "Carisma",
            "Magia": "Carisma",
            "Conhecimento": "Inteligência",
            "Ofício": "Inteligência",
            "Percepção": "Sabedoria",
            "Furtividade": "Destreza",
            "Reflexos": "Destreza"
        },
        "habilidades_classe": {
            "Inspiração de Bardo": "Dá bônus para aliados em testes e ataques",
            "Contramágica": "Anula ou reduz os efeitos de magias adversárias",
            "Conhecimento de Bardo": "Permite aprender e utilizar habilidades diversas"
        }
    },
    {
        "name": "Druida",
        "hp": 14,
        "forca": 12,
        "destreza": 10,
        "defense": 4,
        "pericias": {
            "Sobrevivência": "Sabedoria",
            "Cura": "Sabedoria",
            "Magia": "Sabedoria",
            "Conhecimento (Natureza)": "Inteligência",
            "Ofício": "Inteligência",
            "Percepção": "Sabedoria",
            "Cavalgar": "Destreza",
            "Fortitude": "Constituição"
        },
        "habilidades_classe": {
            "Forma Selvagem": "Permite transformar-se em animais",
            "Magia Natural": "Conjura magias relacionadas à natureza",
            "Companheiro Animal": "Possui um animal companheiro que o auxilia em combate"
        }
    },
    {
        "name": "Monge",
        "hp": 14,
        "forca": 12,
        "destreza": 14,
        "defense": 5,
        "pericias": {
            "Acrobacia": "Destreza",
            "Luta": "Força",
            "Fortitude": "Constituição",
            "Percepção": "Sabedoria",
            "Furtividade": "Destreza",
            "Reflexos": "Destreza",
            "Sobrevivência": "Sabedoria",
            "Conhecimento": "Inteligência"
        },
        "habilidades_classe": {
            "Ataque Desarmado": "Causa dano mesmo sem armas",
            "Evasão": "Reduz o dano de ataques em área",
            "Resistência ao Veneno": "Aumenta resistência a venenos e doenças"
        }
    },
    {
        "name": "Patrulheiro",
        "hp": 16,
        "forca": 12,
        "destreza": 14,
        "defense": 4,
        "pericias": {
            "Sobrevivência": "Sabedoria",
            "Cavalgar": "Destreza",
            "Furtividade": "Destreza",
            "Luta": "Força",
            "Pontaria": "Destreza",
            "Percepção": "Sabedoria",
            "Reflexos": "Destreza",
            "Conhecimento (Natureza)": "Inteligência"
        },
        "habilidades_classe": {
            "Inimigo Favorito": "Bônus contra criaturas específicas",
            "Rastrear": "Permite seguir pistas e rastros com facilidade",
            "Combate com Duas Armas": "Permite utilizar duas armas de forma eficaz"
        }
    },
    {
        "name": "Bruxo",
        "hp": 14,
        "forca": 8,
        "destreza": 10,
        "defense": 3,
        "pericias": {
            "Magia": "Carisma",
            "Enganação": "Carisma",
            "Intimidação": "Carisma",
            "Conhecimento": "Inteligência",
            "Ofício": "Inteligência",
            "Percepção": "Sabedoria",
            "Reflexos": "Destreza",
            "Furtividade": "Destreza"
        },
        "habilidades_classe": {
            "Pacto Sombrio": "Recebe poderes através de um pacto com uma entidade poderosa",
            "Magia Sombria": "Conjura magias sombrias e perigosas",
            "Resistência Sombria": "Aumenta resistência contra ataques e efeitos sombrios"
        }
    },
    {
        "name": "Feiticeiro",
        "hp": 12,
        "forca": 8,
        "destreza": 12,
        "defense": 3,
        "pericias": {
            "Magia": "Carisma",
            "Enganação": "Carisma",
            "Intimidação": "Carisma",
            "Conhecimento": "Inteligência",
            "Ofício": "Inteligência",
            "Percepção": "Sabedoria",
            "Reflexos": "Destreza",
            "Furtividade": "Destreza"
        },
        "habilidades_classe": {
            "Magia Inata": "Conjura magias através de poder inato",
            "Sangue Místico": "Recebe bônus em magia devido a herança mágica",
            "Resistência a Magia": "Aumenta resistência contra magias adversárias"
        }
    }
]

    db.classes.insert_many(classes)


def get_class_by_id(db, class_id):
    return db.classes.find_one({"_id": ObjectId(class_id)})
