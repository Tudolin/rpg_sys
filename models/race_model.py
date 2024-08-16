from bson import ObjectId


def create_default_races(db):
    races = [
        {
            "name": "Aggelus", 
            "hp_bonus": 0, 
            "forca_bonus": 0, 
            "destreza_bonus": 0, 
            "constituicao_bonus": 0, 
            "inteligencia_bonus": 0, 
            "sabedoria_bonus": 4, 
            "carisma_bonus": 2,
            "habilidades_inatas": {
                "Visão No Escuro": "Enxergam no escuro a até 18m, mas apenas em preto e branco",
                "Magia de Luz": "Pode lançar a magia de luz que ilumina um raio de 18m",
                "Resistência a Frio, Ácido e Eletricidade": "Recebe -5 de dano causado por esses efeitos"
            }
        },
        {
            "name": "Elfo", 
            "hp_bonus": 0, 
            "forca_bonus": 0, 
            "destreza_bonus": 4, 
            "constituicao_bonus": -2, 
            "inteligencia_bonus": 2, 
            "sabedoria_bonus": 0, 
            "carisma_bonus": 0,
            "habilidades_inatas": {
                "Percepção Avançada": "+4 em testes de Identificar Magia e Percepção",
                "Dádiva Mágica": "+4 em testes de Vontade contra Encantamentos",
                "Visão Penumbra": "Um Elfo ignora camuflagem (mas não camuflagem total) por escuridão"
            }
        },
        {
            "name": "Humano", 
            "hp_bonus": 0, 
            "forca_bonus": 0, 
            "destreza_bonus": 0, 
            "constituicao_bonus": 0, 
            "inteligencia_bonus": 0, 
            "sabedoria_bonus": 0, 
            "carisma_bonus": 0,
            "habilidades_inatas": {
                "Versatilidade": "Ganha 1 ponto de atributo adicional em qualquer atributo de sua escolha",
                "Adaptabilidade": "Ganha uma perícia adicional a sua escolha"
            }
        },
        {
            "name": "Goblin", 
            "hp_bonus": 0, 
            "forca_bonus": 0, 
            "destreza_bonus": 4, 
            "constituicao_bonus": 0, 
            "inteligencia_bonus": 2, 
            "sabedoria_bonus": 0, 
            "carisma_bonus": -2,
            "habilidades_inatas": {
                "Engenhoso": "Você não sofre penalidades em testes de perícia por não usar kits. Se usar o kit, recebe +2 no teste de perícia",
                "Espelunqueiro": "Você recebe visão no escuro e deslocamento de escalada igual ao seu deslocamento terrestre",
                "Rato das Ruas": "Você recebe +2 em Fortitude e sua recuperação de PV e PM"
            }
        },
        {
            "name": "Anão", 
            "hp_bonus": 4, 
            "forca_bonus": 0, 
            "destreza_bonus": 0, 
            "constituicao_bonus": 2, 
            "inteligencia_bonus": 0, 
            "sabedoria_bonus": 0, 
            "carisma_bonus": -2,
            "habilidades_inatas": {
                "Resistência a Veneno": "+2 em testes de resistência contra venenos",
                "Conhecimento das Rochas": "+2 em testes de Conhecimento (geografia) relacionados a montanhas e subterrâneos",
                "Visão no Escuro": "Enxerga no escuro a até 18m, mas apenas em preto e branco"
            }
        },
        {
            "name": "Minotauro", 
            "hp_bonus": 0, 
            "forca_bonus": 4, 
            "destreza_bonus": 0, 
            "constituicao_bonus": 2, 
            "inteligencia_bonus": 0, 
            "sabedoria_bonus": 0, 
            "carisma_bonus": -2,
            "habilidades_inatas": {
                "Chifres": "Ataque natural que causa dano letal igual ao seu bônus de Força",
                "Visão no Escuro": "Enxerga no escuro a até 18m, mas apenas em preto e branco",
                "Resistência Natural": "+2 em testes de Fortitude"
            }
        },
        {
            "name": "Lefou", 
            "hp_bonus": 0, 
            "forca_bonus": 0, 
            "destreza_bonus": 0, 
            "constituicao_bonus": 2, 
            "inteligencia_bonus": 0, 
            "sabedoria_bonus": 0, 
            "carisma_bonus": -2,
            "habilidades_inatas": {
                "Mutação": "Ganha uma mutação aleatória",
                "Visão no Escuro": "Enxerga no escuro a até 18m, mas apenas em preto e branco",
                "Resistência ao Caos": "+2 em testes de resistência contra efeitos caóticos"
            }
        },
        {
        "name": "Meio-Orc", 
        "hp_bonus": 0, 
        "forca_bonus": 2, 
        "destreza_bonus": 0, 
        "constituicao_bonus": 2, 
        "inteligencia_bonus": -2, 
        "sabedoria_bonus": 0, 
        "carisma_bonus": -2,
        "habilidades_inatas": {
            "Visão no Escuro": "Enxerga no escuro a até 18m, mas apenas em preto e branco.",
            "Fúria Orc": "Quando seus pontos de vida caem para 0 ou menos, você pode continuar a lutar por mais um turno como se tivesse 1 PV.",
            "Intimidação Orc": "Recebe +2 em testes de Intimidação."
        }
    },
    {
        "name": "Gnomo", 
        "hp_bonus": 0, 
        "forca_bonus": -2, 
        "destreza_bonus": 2, 
        "constituicao_bonus": 2, 
        "inteligencia_bonus": 0, 
        "sabedoria_bonus": 0, 
        "carisma_bonus": 0,
        "habilidades_inatas": {
            "Magia Gnômica": "Pode lançar a magia Prestidigitação e Ilusão Menor 1 vez ao dia.",
            "Visão no Escuro": "Enxerga no escuro a até 18m, mas apenas em preto e branco.",
            "Resistência a Ilusões": "+2 em testes de resistência contra magias e efeitos de ilusão."
        }
    },
    {
        "name": "Tiefling", 
        "hp_bonus": 0, 
        "forca_bonus": 0, 
        "destreza_bonus": 2, 
        "constituicao_bonus": 0, 
        "inteligencia_bonus": 2, 
        "sabedoria_bonus": 0, 
        "carisma_bonus": -2,
        "habilidades_inatas": {
            "Resistência Infernal": "Recebe resistência 5 a fogo.",
            "Magia Sombria": "Pode lançar a magia Escuridão uma vez ao dia.",
            "Visão no Escuro": "Enxerga no escuro a até 18m, mas apenas em preto e branco."
        }
    },
    {
        "name": "Halfling", 
        "hp_bonus": 0, 
        "forca_bonus": -2, 
        "destreza_bonus": 2, 
        "constituicao_bonus": 0, 
        "inteligencia_bonus": 0, 
        "sabedoria_bonus": 0, 
        "carisma_bonus": 2,
        "habilidades_inatas": {
            "Sortudo": "Pode rolar novamente um teste de ataque, teste de habilidade ou teste de resistência em que tenha tirado 1 natural.",
            "Pequeno e Ágil": "+2 em testes de Furtividade e Esquiva.",
            "Visão Penumbra": "Ignora camuflagem (mas não camuflagem total) por escuridão."
        }
    }
    ]

    db.races.insert_many(races)

def get_race_by_id(db, race_id):
    return db.races.find_one({"_id": ObjectId(race_id)})
