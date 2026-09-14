from local_db import ObjectId

# Fixed ids for the built-in medieval classes, matching the ids that
# abilities_model.py's class ability grants already reference (see the
# matching comment in race_model.py for why this matters).
_LEGACY_CLASS_IDS = [
    "66bf65914681d1641b7a7222",  # Guerreiro
    "66bf65914681d1641b7a7223",  # Mago
    "66bf65914681d1641b7a7224",  # Ladino
    "66bf65914681d1641b7a7225",  # Clérigo
    "66bf65914681d1641b7a7226",  # Paladino
    "66bf65914681d1641b7a7227",  # Bardo
    "66bf65914681d1641b7a7228",  # Druida
    "66bf65914681d1641b7a7229",  # Monge
    "66bf65914681d1641b7a722a",  # Patrulheiro
    "66bf65914681d1641b7a722b",  # Bruxo
    "66bf65914681d1641b7a722c",  # Feiticeiro
    "66bf65914681d1641b7a722d",  # Bárbaro
    "66bf65914681d1641b7a722e",  # Cavaleiro
    "66bf65914681d1641b7a722f",  # Xamã
    "66bf65914681d1641b7a7230",  # Alquimista
    "66bf65914681d1641b7a7231",  # Samurai
    "66bf65914681d1641b7a7232",  # Metamorfo
]


def create_default_classes(db):
    classes = [
    {
        "name": "Guerreiro",
        "hp": 20,
        "mana": 5,
        "energia": 10,
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
        "mana": 25,
        "energia": 5,
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
        "mana": 10,
        "energia": 20,
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
        "mana": 15,
        "energia": 8,
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
        "mana": 10,
        "energia": 10,
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
        "mana": 15,
        "energia": 10,
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
        "mana": 20,
        "energia": 10,
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
        "mana": 10,
        "energia": 15,
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
        "mana": 10,
        "energia": 15,
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
        "mana": 20,
        "energia": 10,
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
        "mana": 20,
        "energia": 10,
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
    },
    {
        "name": "Bárbaro",
        "hp": 20,
        "mana": 5,
        "energia": 15,
        "forca": 18,
        "destreza": 12,
        "defense": 4,
        "pericias": {
            "Luta": "Força",
            "Fortitude": "Constituição",
            "Sobrevivência": "Sabedoria",
            "Percepção": "Sabedoria",
            "Atletismo": "Força",
            "Intimidação": "Carisma",
            "Reflexos": "Destreza"
        },
        "habilidades_classe": {
            "Fúria": "Aumenta dano e resistência temporariamente, mas fica exausto depois.",
            "Movimento Rápido": "Aumenta o deslocamento base.",
            "Resistência ao Dano": "Reduz dano de fontes não mágicas."
        }
    },
    {
        "name": "Cavaleiro",
        "hp": 18,
        "mana": 8,
        "energia": 10,
        "forca": 16,
        "destreza": 8,
        "defense": 6,
        "pericias": {
            "Luta": "Força",
            "Cavalgar": "Destreza",
            "Guerra": "Inteligência",
            "Diplomacia": "Carisma",
            "Fortitude": "Constituição",
            "Intimidação": "Carisma",
            "Percepção": "Sabedoria"
        },
        "habilidades_classe": {
            "Desafiar Inimigo": "Pode desafiar um inimigo, forçando-o a atacar o cavaleiro.",
            "Presença Inspiradora": "Concede bônus a aliados próximos.",
            "Montaria Especial": "Ganha uma montaria que aumenta em força e resistência conforme o nível."
        }
    },
    {
        "name": "Xamã",
        "hp": 14,
        "mana": 18,
        "energia": 8,
        "forca": 10,
        "destreza": 10,
        "defense": 3,
        "pericias": {
            "Magia": "Sabedoria",
            "Conhecimento (Espíritos)": "Sabedoria",
            "Cura": "Sabedoria",
            "Sobrevivência": "Sabedoria",
            "Intimidação": "Carisma",
            "Percepção": "Sabedoria",
            "Fortitude": "Constituição"
        },
        "habilidades_classe": {
            "Conjuração Espiritual": "Invoca espíritos para assistência em combate ou em feitiços.",
            "Comando Espiritual": "Pode comandar espíritos para realizar tarefas específicas.",
            "Vínculo Espiritual": "Forma um vínculo com um espírito que oferece poderes adicionais."
        }
    },
    {
        "name": "Alquimista",
        "hp": 12,
        "mana": 18,
        "energia": 12,
        "forca": 8,
        "destreza": 14,
        "defense": 3,
        "pericias": {
            "Alquimia": "Inteligência",
            "Conhecimento": "Inteligência",
            "Magia": "Inteligência",
            "Ofício": "Inteligência",
            "Furtividade": "Destreza",
            "Percepção": "Sabedoria",
            "Reflexos": "Destreza"
        },
        "habilidades_classe": {
            "Misturas Alquímicas": "Cria poções e elixires com efeitos diversos.",
            "Bomba Alquímica": "Cria bombas que podem causar dano ou efeitos especiais.",
            "Mutagênico": "Concede bônus temporários a atributos, mas com desvantagens."
        }
    },
    {
        "name": "Samurai",
        "hp": 18,
        "mana": 10,
        "energia": 14,
        "forca": 16,
        "destreza": 12,
        "defense": 5,
        "pericias": {
            "Luta": "Força",
            "Cavalgar": "Destreza",
            "Intimidação": "Carisma",
            "Percepção": "Sabedoria",
            "Fortitude": "Constituição",
            "Reflexos": "Destreza",
            "Conhecimento (Guerra)": "Inteligência"
        },
        "habilidades_classe": {
            "Ataque Preciso": "Aumenta a precisão dos ataques, especialmente com espadas.",
            "Resistência ao Medo": "Imunidade a medo e bônus para aliados próximos.",
            "Combate com Duas Armas": "Permite utilizar duas armas de forma eficaz, especialmente katanas e wakizashis."
        }
    },
    {
        "name": "Metamorfo",
        "hp": 16,
        "mana": 10,
        "energia": 15,
        "forca": 14,
        "destreza": 12,
        "defense": 4,
        "pericias": {
            "Furtividade": "Destreza",
            "Luta": "Força",
            "Percepção": "Sabedoria",
            "Reflexos": "Destreza",
            "Magia": "Sabedoria",
            "Conhecimento": "Inteligência",
            "Cura": "Sabedoria",
            "Fortitude": "Constituição"
        },
        "habilidades_classe": {
            "Transformação": "Pode se transformar em diferentes formas, adquirindo as habilidades correspondentes.",
            "Regeneração Rápida": "Recupera pontos de vida rapidamente enquanto estiver transformado.",
            "Aprimoramento de Forma": "Pode melhorar suas formas transformadas, adquirindo habilidades adicionais."
        }
    }
]
    for index, class_data in enumerate(classes):
        # Recast the old flat baseline fields into the generic shape used
        # by the character sheet engine (see game_systems.py / character_model.py).
        class_data["resource_bases"] = {
            "hp": class_data.pop("hp", 0),
            "mana": class_data.pop("mana", 0),
            "energia": class_data.pop("energia", 0),
        }
        class_data["combat_bases"] = {
            "ataque": class_data.pop("forca", 0),
            "defesa": class_data.pop("defense", 0),
        }
        class_data.pop("destreza", None)
        class_data["system_id"] = "medieval"
        if index < len(_LEGACY_CLASS_IDS):
            db.classes.update_one(
                {"_id": ObjectId(_LEGACY_CLASS_IDS[index])},
                {"$set": class_data},
                upsert=True,
            )
        else:
            db.classes.update_one(
                {"name": class_data["name"], "system_id": "medieval"},
                {"$set": class_data},
                upsert=True,
            )


def create_default_classes_other_systems(db):
    """Seed a modest set of classes/archetypes for the non-medieval systems."""
    other_classes = [
        # --- Call of Cthulhu: occupations ---
        {"system_id": "cthulhu", "name": "Detetive Particular", "resource_bases": {"hp": 12, "sanidade": 50, "sorte": 50},
         "pericias": {"Investigação": "Inteligência", "Persuasão": "Educação", "Lei": "Educação", "Arrombamento": "Destreza"},
         "habilidades_classe": {"Instinto Aguçado": "Percebe detalhes que passariam despercebidos."}},
        {"system_id": "cthulhu", "name": "Acadêmico", "resource_bases": {"hp": 9, "sanidade": 55, "sorte": 45},
         "pericias": {"Biblioteca": "Educação", "Ocultismo": "Educação", "Línguas": "Educação", "História": "Educação"},
         "habilidades_classe": {"Erudição": "Bônus ao pesquisar em bibliotecas e arquivos."}},
        {"system_id": "cthulhu", "name": "Jornalista", "resource_bases": {"hp": 10, "sanidade": 50, "sorte": 50},
         "pericias": {"Persuasão": "Educação", "Investigação": "Inteligência", "Furtividade": "Destreza"},
         "habilidades_classe": {"Faro para Notícias": "Encontra pistas com mais facilidade em locais públicos."}},
        {"system_id": "cthulhu", "name": "Médico", "resource_bases": {"hp": 11, "sanidade": 45, "sorte": 45},
         "pericias": {"Medicina": "Educação", "Primeiros Socorros": "Educação", "Psicologia": "Educação"},
         "habilidades_classe": {"Mãos Firmes": "Bônus ao estabilizar feridos em combate."}},
        {"system_id": "cthulhu", "name": "Criminoso", "resource_bases": {"hp": 12, "sanidade": 40, "sorte": 55},
         "pericias": {"Arrombamento": "Destreza", "Intimidação": "Força", "Furtividade": "Destreza"},
         "habilidades_classe": {"Contatos do Submundo": "Conhece alguém em quase todo lugar."}},
        {"system_id": "cthulhu", "name": "Antiquário", "resource_bases": {"hp": 9, "sanidade": 50, "sorte": 50},
         "pericias": {"Avaliação": "Inteligência", "Ocultismo": "Educação", "Persuasão": "Educação"},
         "habilidades_classe": {"Olho Clínico": "Reconhece artefatos e falsificações com facilidade."}},
        {"system_id": "cthulhu", "name": "Policial", "resource_bases": {"hp": 13, "sanidade": 45, "sorte": 45},
         "pericias": {"Lei": "Educação", "Armas de Fogo": "Destreza", "Intimidação": "Força", "Investigação": "Inteligência"},
         "habilidades_classe": {"Autoridade da Farda": "Testemunhas colaboram com mais facilidade."}},
        {"system_id": "cthulhu", "name": "Piloto", "resource_bases": {"hp": 12, "sanidade": 50, "sorte": 50},
         "pericias": {"Pilotagem": "Destreza", "Mecânica": "Inteligência", "Navegação": "Inteligência"},
         "habilidades_classe": {"Mãos no Manche": "Bônus em manobras arriscadas de pilotagem."}},
        {"system_id": "cthulhu", "name": "Militar", "resource_bases": {"hp": 15, "sanidade": 40, "sorte": 45},
         "pericias": {"Armas de Fogo": "Destreza", "Tática": "Educação", "Sobrevivência": "Constituição"},
         "habilidades_classe": {"Disciplina de Combate": "Resiste melhor ao pânico sob fogo."}},
        {"system_id": "cthulhu", "name": "Clérigo", "resource_bases": {"hp": 10, "sanidade": 55, "sorte": 50},
         "pericias": {"Ocultismo": "Educação", "Persuasão": "Educação", "Psicologia": "Educação"},
         "habilidades_classe": {"Conforto Espiritual": "Acalma aliados abalados com mais eficácia."}},
        {"system_id": "cthulhu", "name": "Cientista", "resource_bases": {"hp": 9, "sanidade": 50, "sorte": 45},
         "pericias": {"Ciência": "Inteligência", "Medicina": "Educação", "Biblioteca": "Educação"},
         "habilidades_classe": {"Método Científico": "Bônus ao analisar evidências fisicas incomuns."}},
        {"system_id": "cthulhu", "name": "Advogado", "resource_bases": {"hp": 9, "sanidade": 50, "sorte": 50},
         "pericias": {"Lei": "Educação", "Persuasão": "Educação", "Avaliação": "Inteligência"},
         "habilidades_classe": {"Conhece Seus Direitos": "Bônus para negociar com autoridades."}},
        {"system_id": "cthulhu", "name": "Marinheiro", "resource_bases": {"hp": 14, "sanidade": 45, "sorte": 50},
         "pericias": {"Pilotagem": "Destreza", "Mecânica": "Inteligência", "Sobrevivência": "Constituição"},
         "habilidades_classe": {"Pernas do Mar": "Nunca perde o equilíbrio em terrenos instáveis."}},

        # --- Western: archetypes ---
        {"system_id": "western", "name": "Pistoleiro", "resource_bases": {"hp": 18, "determinacao": 10}, "combat_bases": {"pontaria": 15},
         "pericias": {"Pontaria": "Destreza", "Intimidação": "Carisma", "Reflexos": "Destreza"},
         "habilidades_classe": {"Saque Rápido": "Atira primeiro em confrontos diretos."}},
        {"system_id": "western", "name": "Xerife", "resource_bases": {"hp": 20, "determinacao": 14}, "combat_bases": {"pontaria": 10},
         "pericias": {"Autoridade": "Carisma", "Investigação": "Sagacidade", "Pontaria": "Destreza"},
         "habilidades_classe": {"Mão da Lei": "Aliados próximos recebem bônus para resistir à intimidação."}},
        {"system_id": "western", "name": "Fora-da-Lei", "resource_bases": {"hp": 16, "determinacao": 12}, "combat_bases": {"pontaria": 12},
         "pericias": {"Furtividade": "Destreza", "Cavalgar": "Destreza", "Sobrevivência": "Sagacidade"},
         "habilidades_classe": {"Fuga Ágil": "Bônus para escapar de perseguições a cavalo."}},
        {"system_id": "western", "name": "Caçador de Recompensas", "resource_bases": {"hp": 18, "determinacao": 10}, "combat_bases": {"pontaria": 14},
         "pericias": {"Rastrear": "Sagacidade", "Pontaria": "Destreza", "Intimidação": "Força"},
         "habilidades_classe": {"Nunca Erra o Alvo": "Bônus ao perseguir um alvo marcado."}},
        {"system_id": "western", "name": "Cartola", "resource_bases": {"hp": 12, "determinacao": 16}, "combat_bases": {"pontaria": 8},
         "pericias": {"Enganação": "Carisma", "Percepção": "Sagacidade", "Persuasão": "Carisma"},
         "habilidades_classe": {"Cartas Marcadas": "Vantagem em jogos de azar e leitura de blefes."}},
        {"system_id": "western", "name": "Curandeira do Oeste", "resource_bases": {"hp": 14, "determinacao": 14}, "combat_bases": {"pontaria": 6},
         "pericias": {"Medicina": "Sagacidade", "Sobrevivência": "Sagacidade", "Persuasão": "Carisma"},
         "habilidades_classe": {"Remédios da Terra": "Cura ferimentos leves sem precisar de suprimentos."}},
        {"system_id": "western", "name": "Forasteiro", "resource_bases": {"hp": 16, "determinacao": 12}, "combat_bases": {"pontaria": 11},
         "pericias": {"Sobrevivência": "Sagacidade", "Rastrear": "Sagacidade", "Furtividade": "Destreza"},
         "habilidades_classe": {"Andarilho Solitário": "Nunca fica perdido em terreno selvagem."}},
        {"system_id": "western", "name": "Batedor Indígena", "resource_bases": {"hp": 16, "determinacao": 12}, "combat_bases": {"pontaria": 12},
         "pericias": {"Rastrear": "Sagacidade", "Sobrevivência": "Sagacidade", "Cavalgar": "Destreza"},
         "habilidades_classe": {"Um com a Terra": "Lê sinais que ninguém mais percebe."}},
        {"system_id": "western", "name": "Garimpeiro", "resource_bases": {"hp": 15, "determinacao": 10}, "combat_bases": {"pontaria": 8},
         "pericias": {"Sobrevivência": "Sagacidade", "Ofício": "Força", "Avaliação": "Sagacidade"},
         "habilidades_classe": {"Faro para Ouro": "Sempre encontra algo de valor onde outros não veem nada."}},
        {"system_id": "western", "name": "Dono de Saloon", "resource_bases": {"hp": 12, "determinacao": 16}, "combat_bases": {"pontaria": 7},
         "pericias": {"Persuasão": "Carisma", "Percepção": "Sagacidade", "Enganação": "Carisma"},
         "habilidades_classe": {"Olhos e Ouvidos da Cidade": "Sempre sabe o que anda se falando no povoado."}},
        {"system_id": "western", "name": "Pregador", "resource_bases": {"hp": 14, "determinacao": 18}, "combat_bases": {"pontaria": 6},
         "pericias": {"Persuasão": "Carisma", "Intuição": "Sagacidade", "Medicina": "Sagacidade"},
         "habilidades_classe": {"Palavra Inspiradora": "Fortalece a determinação de quem ouve seu sermão."}},
        {"system_id": "western", "name": "Engenheiro Ferroviário", "resource_bases": {"hp": 14, "determinacao": 10}, "combat_bases": {"pontaria": 8},
         "pericias": {"Ofício": "Força", "Mecânica": "Sagacidade", "Percepção": "Sagacidade"},
         "habilidades_classe": {"Solução Improvisada": "Conserta ou constrói algo com o que tiver em mãos."}},

        # --- Cyberpunk: roles ---
        {"system_id": "cyberpunk", "name": "Solo", "resource_bases": {"hp": 20, "humanidade": 40, "energia": 15}, "combat_bases": {"ataque": 16},
         "pericias": {"Combate": "Reflexos", "Táticas": "Inteligência", "Intimidação": "Frieza"},
         "habilidades_classe": {"Reflexos de Combate": "Age primeiro em situações de perigo."}},
        {"system_id": "cyberpunk", "name": "Netrunner", "resource_bases": {"hp": 12, "humanidade": 35, "energia": 25}, "combat_bases": {"ataque": 6},
         "pericias": {"Hacking": "Técnica", "Eletrônica": "Técnica", "Interface": "Inteligência"},
         "habilidades_classe": {"Mergulho Profundo": "Acessa sistemas protegidos com mais facilidade."}},
        {"system_id": "cyberpunk", "name": "Fixer", "resource_bases": {"hp": 14, "humanidade": 45, "energia": 15}, "combat_bases": {"ataque": 8},
         "pericias": {"Persuasão": "Frieza", "Streetwise": "Inteligência", "Negociação": "Frieza"},
         "habilidades_classe": {"Rede de Contatos": "Sempre conhece alguém que pode ajudar."}},
        {"system_id": "cyberpunk", "name": "Rockerboy", "resource_bases": {"hp": 14, "humanidade": 50, "energia": 15}, "combat_bases": {"ataque": 8},
         "pericias": {"Performance": "Frieza", "Persuasão": "Frieza", "Percepção": "Inteligência"},
         "habilidades_classe": {"Voz do Povo": "Inspira e mobiliza multidões."}},
        {"system_id": "cyberpunk", "name": "Nômade", "resource_bases": {"hp": 18, "humanidade": 45, "energia": 15}, "combat_bases": {"ataque": 12},
         "pericias": {"Pilotagem": "Reflexos", "Mecânica": "Técnica", "Sobrevivência": "Vontade"},
         "habilidades_classe": {"Família de Estrada": "Conta com apoio do seu clã nômade."}},
        {"system_id": "cyberpunk", "name": "Exec", "resource_bases": {"hp": 14, "humanidade": 35, "energia": 15}, "combat_bases": {"ataque": 10},
         "pericias": {"Negociação": "Frieza", "Liderança": "Vontade", "Etiqueta": "Frieza"},
         "habilidades_classe": {"Imunidade Corporativa": "Recursos e proteção legal de uma megacorporação."}},
        {"system_id": "cyberpunk", "name": "Tech", "resource_bases": {"hp": 14, "humanidade": 45, "energia": 20}, "combat_bases": {"ataque": 6},
         "pericias": {"Mecânica": "Técnica", "Eletrônica": "Técnica", "Ofício": "Técnica"},
         "habilidades_classe": {"Conserto de Campo": "Repara qualquer coisa com o que tiver à mão."}},
        {"system_id": "cyberpunk", "name": "Medtech", "resource_bases": {"hp": 14, "humanidade": 45, "energia": 20}, "combat_bases": {"ataque": 6},
         "pericias": {"Medicina": "Técnica", "Cirurgia de Implantes": "Técnica", "Farmacologia": "Inteligência"},
         "habilidades_classe": {"Mãos que Salvam (ou Não)": "Estabiliza ou incapacita com precisão cirúrgica."}},
        {"system_id": "cyberpunk", "name": "Media", "resource_bases": {"hp": 12, "humanidade": 45, "energia": 15}, "combat_bases": {"ataque": 6},
         "pericias": {"Investigação": "Inteligência", "Persuasão": "Frieza", "Percepção": "Inteligência"},
         "habilidades_classe": {"Verdade a Qualquer Custo": "Sempre encontra uma forma de furar o cerco da censura."}},
        {"system_id": "cyberpunk", "name": "Lawman", "resource_bases": {"hp": 18, "humanidade": 40, "energia": 15}, "combat_bases": {"ataque": 13},
         "pericias": {"Autoridade": "Frieza", "Armas de Fogo": "Reflexos", "Investigação": "Inteligência"},
         "habilidades_classe": {"Reforços": "Pode chamar apoio policial em momentos críticos."}},
    ]

    for class_data in other_classes:
        db.classes.update_one(
            {"name": class_data["name"], "system_id": class_data["system_id"]},
            {"$set": class_data},
            upsert=True,
        )


def get_classes_by_system(db, system_id):
    return list(db.classes.find({"system_id": system_id}))


def get_class_by_id(db, class_id):
    return db.classes.find_one({"_id": ObjectId(class_id)})
