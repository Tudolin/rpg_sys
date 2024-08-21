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
            },
            "resumo":"Seres extraplanares bondosos, também conhecidos como “anjos” ou “celestiais”, muitas vezes apaixonam-se por mortais — ou são capturados por estes — e produzem descendentes, transmitindo sua herança divina. Em outros casos, o nascimento de um Filho dos Anjos é provocado pela intervenção direta de uma divindade; este ser especial seria um enviado santo, destinado a lutar pelo bem e cumprir um grande destino. Seja como for, estas criaturas são chamadas de Aggelus."
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
            },
            "resumo":"Esta raça antiga e mágica foi uma das primeiras criadas pelos deuses. São graciosos e sagazes, mas também excessivamente orgulhosos — sempre acreditaram ser melhores que os outros povos, nunca aceitando alianças. Essa arrogância custou-lhes caro quando sua nação foi arrasada por seus inimigos, os goblinoides."
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
            },
            "resumo":"Humanos são conhecidos por sua adaptabilidade e versatilidade, podendo se destacar em qualquer área que escolham."
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
            },
            "resumo":"Goblins são criaturas engenhosas e ágeis, adaptadas para sobreviver nos ambientes mais inóspitos."
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
            },
            "resumo":"Povo recluso e próximo das montanhas e rochas, os anões habitam o reino subterrâneo de Doherimm, onde escavam riquezas. No entanto, são gente simples: gostam de esculpir rocha, trabalhar o metal e entalhar joias — além de uma boa briga e uma cerveja bem tirada!"
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
            },
            "resumo":"Minotauros são criaturas poderosas e resistentes, conhecidas por sua força bruta e resistência natural."
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
            },
            "resumo":"Lefous são seres mutantes com resistência natural ao caos, muitas vezes temidos por suas estranhas habilidades."
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
        },
        "resumo":"O meio-orc é o fruto da rara união entre um orc e um humano. São criaturas abrutalhadas, simples e fortes, mas dotadas de intelecto e discernimento. Compartilham traços selvagens dos orcs (presas, focinho, pêlos) e características físicas dos humanos (rosto claramente inteligente, mãos e pés sem garras). São vítimas de grande preconceito, mas sua enorme força faz com que sejam poderosos heróis, quando se dedicam a isso. O caminho do aventureiro é muito comum entre os meio-orcs, sendo uma das únicas maneiras dessas criaturas obterem respeito e prosperidade]. Costumam nascer em grande quantidade no reino de Lomatubar, devido a grande incidência de humanos e orcs neste reino"
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
        },
        "resumo":"O gnomo é uma raça ainda mais baixa que os anões, que não existe como nativa em Arton. O único representante conhecido dessa raça é o famoso Lorde Niebling, transportado misteriosamente até Arton de um mundo distante."
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
        },
        "resumo":"Criaturas de aparência infernal, herdadas de antepassados que ousaram fazer pactos com diabos para se tornarem mais poderosos. Todo Tiefling carrega essa maldição e esse poder, desde cedo aprende a viver a margem da sociedade e esconder sua aparência."
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
        },
        "resumo":"Os halflings, também chamados de hobbits ou apenas pequeninos, são uma espécie pacata e bonachona, alegre e acolhedora, baixa (ainda menores que os anões e rechonchuda, fraca, mas muito ágil e resistente a magia. Têm pés grandes e peludos, e nunca usam sapatos. Os halflings vivem em comunidades isoladas dentro do Reinado, mas nunca participam de política ou das grandes decisões dos reinos. Apreciam boa comida, conforto e paz, raramente deixando suas casas"
    }
    ]
    for race_data in races:
        db.races.update_one(
            {"name": race_data["name"]},
            {"$set": race_data},
            upsert=True  # Isso garante que o documento seja inserido se não existir
        )
    # db.races.insert_many(races)

def get_race_by_id(db, race_id):
    return db.races.find_one({"_id": ObjectId(race_id)})
