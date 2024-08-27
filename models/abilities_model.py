from bson import ObjectId


def create_default_abilities(db): 
    abilities = [
        {
            "name": "Visão No Escuro",
            "description": "Enxergam no escuro a até 18m, mas apenas em preto e branco.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7235"), ObjectId("66bf65924681d1641b7a7238"), ObjectId("66bf65924681d1641b7a723a"), ObjectId("66bf65924681d1641b7a723b"), ObjectId("66bf65924681d1641b7a723c"), ObjectId("66bf65924681d1641b7a723d"), ObjectId("66bf65924681d1641b7a723e"), ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Magia de Luz",
            "description": "Pode lançar a magia de luz que ilumina um raio de 18m.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7235")]
            },
            "cost": {
                "mana": 10,
                "energy": 0
            }
        },
        {
            "name": "Resistência a Frio, Ácido e Eletricidade",
            "description": "Recebe -5 de dano causado por esses efeitos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7235")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Percepção Avançada",
            "description": "+4 em testes de Identificar Magia e Percepção.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7236")]
            },
            "cost": {
                "mana": 5,
                "energy": 0
            }
        },
        {
            "name": "Dádiva Mágica",
            "description": "+4 em testes de Vontade contra Encantamentos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7236")]
            },
            "cost": {
                "mana": 5,
                "energy": 0
            }
        },
        {
            "name": "Visão Penumbra",
            "description": "Um Elfo ignora camuflagem (mas não camuflagem total) por escuridão.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7236"), ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Versatilidade",
            "description": "Ganha 1 ponto de atributo adicional em qualquer atributo de sua escolha.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Adaptabilidade",
            "description": "Ganha uma perícia adicional à sua escolha.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Engenhoso",
            "description": "Não sofre penalidades em testes de perícia por não usar kits. Se usar o kit, recebe +2 no teste de perícia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7238")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Espelunqueiro",
            "description": "Recebe visão no escuro e deslocamento de escalada igual ao seu deslocamento terrestre.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7238")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Rato das Ruas",
            "description": "Recebe +2 em Fortitude e sua recuperação de PV e PM.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7238")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resistência a Veneno",
            "description": "+2 em testes de resistência contra venenos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Chifres",
            "description": "Ataque natural que causa dano letal igual ao seu bônus de Força.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resistência Natural",
            "description": "+2 em testes de Fortitude.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Mutação",
            "description": "Ganha uma mutação aleatória.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Resistência ao Caos",
            "description": "+2 em testes de resistência contra efeitos caóticos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Fúria Orc",
            "description": "Quando seus pontos de vida caem para 0 ou menos, você pode continuar a lutar por mais um turno como se tivesse 1 PV.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Intimidação Orc",
            "description": "Recebe +2 em testes de Intimidação.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Magia Gnômica",
            "description": "Pode lançar a magia Prestidigitação e Ilusão Menor 1 vez ao dia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 10,
                "energy": 0
            }
        },
        {
            "name": "Resistência a Ilusões",
            "description": "+2 em testes de resistência contra magias e efeitos de ilusão.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resistência Infernal",
            "description": "Recebe resistência 5 a fogo.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Magia Sombria",
            "description": "Pode lançar a magia Escuridão uma vez ao dia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 10,
                "energy": 0
            }
        },
        {
            "name": "Sortudo",
            "description": "Pode rolar novamente um teste de ataque, teste de habilidade ou teste de resistência em que tenha tirado 1 natural.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Pequeno e Ágil",
            "description": "+2 em testes de Furtividade e Esquiva.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Ataque Preciso",
            "description": "Aumenta a precisão dos ataques.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7222"), ObjectId("66bf65914681d1641b7a7232")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Resistência a Dano",
            "description": "Reduz o dano recebido em combate.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7222"), ObjectId("66bf65914681d1641b7a722d")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Maestria em Armas",
            "description": "Aumenta a eficácia das armas utilizadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7222")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Magia Arcana",
            "description": "Permite lançar feitiços e manipular energia mágica.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7223"), ObjectId("66bf65914681d1641b7a722c"), ObjectId("66bf65914681d1641b7a722b")]
            },
            "cost": {
                "mana": 20,
                "energy": 0
            }
        },
        {
            "name": "Conhecimento Mágico",
            "description": "Aumenta o entendimento e o uso de magia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7223"), ObjectId("66bf65914681d1641b7a722b"), ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 10,
                "energy": 0
            }
        },
        {
            "name": "Mana Aprimorado",
            "description": "Aumenta a quantidade de mana disponível.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7223")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Ataque Furtivo",
            "description": "Dano extra ao atacar inimigos desatentos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7224")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Evasão",
            "description": "Reduz o dano de ataques em área.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7224"), ObjectId("66bf65914681d1641b7a7229")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Desarmar Armadilhas",
            "description": "Permite desarmar armadilhas e mecanismos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7224")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Canalizar Energia",
            "description": "Recupera pontos de vida ou causa dano a mortos-vivos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7225")]
            },
            "cost": {
                "mana": 10,
                "energy": 10
            }
        },
        {
            "name": "Milagre",
            "description": "Permite lançar feitiços divinos poderosos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7225")]
            },
            "cost": {
                "mana": 20,
                "energy": 0
            }
        },
        {
            "name": "Abençoar",
            "description": "Aumenta as habilidades de aliados temporariamente.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7225"), ObjectId("66bf65914681d1641b7a7226")]
            },
            "cost": {
                "mana": 5,
                "energy": 5
            }
        },
        {
            "name": "Imposição das Mãos",
            "description": "Cura a si mesmo ou a outros com um toque.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7226")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Aura de Coragem",
            "description": "Imunidade ao medo e bônus para aliados próximos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7226")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Golpe Divino",
            "description": "Causa dano extra contra criaturas malignas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7226")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Inspiração de Bardo",
            "description": "Dá bônus para aliados em testes e ataques.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7227")]
            },
            "cost": {
                "mana": 5,
                "energy": 10
            }
        },
        {
            "name": "Contramágica",
            "description": "Anula ou reduz os efeitos de magias adversárias.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7227")]
            },
            "cost": {
                "mana": 10,
                "energy": 5
            }
        },
        {
            "name": "Conhecimento de Bardo",
            "description": "Permite aprender e utilizar habilidades diversas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7227")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Forma Selvagem",
            "description": "Permite transformar-se em animais.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7231")]
            },
            "cost": {
                "mana": 10,
                "energy": 10
            }
        },
        {
            "name": "Magia Natural",
            "description": "Conjura magias relacionadas à natureza.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7231")]
            },
            "cost": {
                "mana": 15,
                "energy": 0
            }
        },
        {
            "name": "Companheiro Animal",
            "description": "Possui um animal companheiro que o auxilia em combate.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7231")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Ataque Desarmado",
            "description": "Causa dano mesmo sem armas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7229")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Resistência ao Veneno",
            "description": "Aumenta resistência a venenos e doenças.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7229")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Inimigo Favorito",
            "description": "Bônus contra criaturas específicas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722a")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Rastrear",
            "description": "Permite seguir pistas e rastros com facilidade.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Combate com Duas Armas",
            "description": "Permite utilizar duas armas de forma eficaz.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722a"), ObjectId("66bf65914681d1641b7a7232")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Pacto Sombrio",
            "description": "Recebe poderes através de um pacto com uma entidade poderosa.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722b")]
            },
            "cost": {
                "mana": 20,
                "energy": 0
            }
        },
        {
            "name": "Resistência Sombria",
            "description": "Aumenta resistência contra ataques e efeitos sombrios.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722b")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Magia Inata",
            "description": "Conjura magias através de poder inato.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 15,
                "energy": 0
            }
        },
        {
            "name": "Sangue Místico",
            "description": "Recebe bônus em magia devido a herança mágica.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 10,
                "energy": 0
            }
        },
        {
            "name": "Resistência a Magia",
            "description": "Aumenta resistência contra magias adversárias.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Fúria",
            "description": "Aumenta dano e resistência temporariamente, mas fica exausto depois.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722d")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Movimento Rápido",
            "description": "Aumenta o deslocamento base.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722d")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Desafiar Inimigo",
            "description": "Pode desafiar um inimigo, forçando-o a atacar o cavaleiro.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722e")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Presença Inspiradora",
            "description": "Concede bônus a aliados próximos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722e")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Montaria Especial",
            "description": "Ganha uma montaria que aumenta em força e resistência conforme o nível.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722e")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Conjuração Espiritual",
            "description": "Invoca espíritos para assistência em combate ou em feitiços.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722f")]
            },
            "cost": {
                "mana": 15,
                "energy": 5
            }
        },
        {
            "name": "Comando Espiritual",
            "description": "Pode comandar espíritos para realizar tarefas específicas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722f")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Vínculo Espiritual",
            "description": "Forma um vínculo com um espírito que oferece poderes adicionais.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722f")]
            },
            "cost": {
                "mana": 10,
                "energy": 5
            }
        },
        {
            "name": "Misturas Alquímicas",
            "description": "Cria poções e elixires com efeitos diversos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7230")]
            },
            "cost": {
                "mana": 5,
                "energy": 5
            }
        },
        {
            "name": "Bomba Alquímica",
            "description": "Cria bombas que podem causar dano ou efeitos especiais.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7230")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Mutagênico",
            "description": "Concede bônus temporários a atributos, mas com desvantagens.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7230")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Transformação",
            "description": "Pode se transformar em diferentes formas, adquirindo as habilidades correspondentes.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7233")]
            },
            "cost": {
                "mana": 15,
                "energy": 10
            }
        },
        {
            "name": "Regeneração Rápida",
            "description": "Recupera pontos de vida rapidamente enquanto estiver transformado.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7233")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Aprimoramento de Forma",
            "description": "Pode melhorar suas formas transformadas, adquirindo habilidades adicionais.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7233")]
            },
            "cost": {
                "mana": 10,
                "energy": 15
            }
        }
    ]


    for ability in abilities:
        db.abilities.update_one(
            {"name": ability["name"]},
            {"$set": ability},
            upsert=True
        )

def get_ability_by_id(db, ability_id):
    return db.abilities.find_one({"_id": ObjectId(ability_id)})

def get_abilities_by_race(db, race_id):
    return list(db.abilities.find({"related_to.race_ids": ObjectId(race_id)}))

def get_abilities_by_class(db, class_id):
    return list(db.abilities.find({"related_to.class_ids": ObjectId(class_id)}))
