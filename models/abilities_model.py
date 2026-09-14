from local_db import ObjectId


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
            "description": "Pode lançar a magia de Ilusão.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 15,
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
            "description": "Magia da escuridão, cega todos os inimigos por 1 rodada.",
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
                "race_ids": [ObjectId("66bf65924681d1641b7a723f"), ObjectId("66bf65924681d1641b7a723d"), ObjectId("66bf65924681d1641b7a7236"), ObjectId("66bf65924681d1641b7a7238"),]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Ataque Preciso",
            "description": "Aumenta a precisão dos ataques, ganhando +3 na rolagem.",
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
            "description": "Reduz o dano recebido em combate em -5.",
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
            "description": "Aumenta a eficácia das armas utilizadas, +3 em qualquer teste de destreza.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7222"), ObjectId("66bf65914681d1641b7a7232")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Magia Arcana",
            "description": "Ataque de luz celestial, causa +10 de dano contra criaturas diabolicas ou das sombras.",
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
            "description": "Aumenta o entendimento e o uso de magia, em testes para decifrar, entender ou desativar armadilhas ou ataques mágicos, recebe +5 na rolagem.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7223"), ObjectId("66bf65914681d1641b7a722b"), ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 4,
                "energy": 4
            }
        },
        {
            "name": "Mana Aprimorado",
            "description": "Aumenta a quantidade de mana disponível em +10.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7223"), ObjectId("66bf65914681d1641b7a722c"), ObjectId("66bf65914681d1641b7a7230"), ObjectId("66bf65914681d1641b7a722b")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Ataque Furtivo",
            "description": "Dano extra ao atacar inimigos desatentos, +5 na rolagem.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7224")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
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
            "description": "Permite desarmar armadilhas e mecanismos sem necessária rolagem.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7224")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Canalizar Energia",
            "description": "Recupera 10 pontos de vida.",
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
            "description": "Feitiço divino, causa +20 de dano contra inimigos demoniacos",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7225")]
            },
            "cost": {
                "mana": 30,
                "energy": 0
            }
        },
        {
            "name": "Abençoar",
            "description": "Aumenta as habilidades de aliados temporariamente, dando a todos +3 em qualquer rolagem.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7225"), ObjectId("66bf65914681d1641b7a7226")]
            },
            "cost": {
                "mana": 10,
                "energy": 10
            }
        },
        {
            "name": "Imposição das Mãos",
            "description": "Cura a si mesmo ou a outros com um toque.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7226"), ObjectId("66bf65914681d1641b7a722c"), ObjectId("66bf65914681d1641b7a7228")]
            },
            "cost": {
                "mana": 5,
                "energy": 10
            }
        },
        {
            "name": "Aura de Coragem",
            "description": "Imunidade ao medo e ilusões por 3 rodadas.",
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
            "description": "Causa dano extra +5 contra criaturas malignas.",
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
            "description": "Dá bônus para aliados em testes e ataques +3 em todas as rolagens.",
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
            "description": "Anula ou reduz os efeitos de magias adversárias em -5.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7227")]
            },
            "cost": {
                "mana": 10,
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
            "name": "Soco na cara",
            "description": "Causa +2 dano mesmo sem armas.",
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
            "description": "Aumenta resistência a venenos e doenças -5 de dano por esses efeitos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a7229")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Rastrear",
            "description": "Permite seguir pistas e rastros com facilidade +5 em rolagens de investigação.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722a")]
            },
            "cost": {
                "mana": 0,
                "energy": 7
            }
        },
        {
            "name": "Combate com Duas Armas",
            "description": "Permite utilizar duas armas de forma eficaz, ao atacar, rola um dado por arma.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722a"), ObjectId("66bf65914681d1641b7a7232")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
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
            "description": "Aumenta resistência contra ataques de efeitos sombrios, tomando -5 de dano.",
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
            "description": "Na prioridade de ataque recebe +4 a rolagem.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 15,
                "energy": 0
            }
        },
        {
            "name": "Resistência a Magia",
            "description": "Aumenta resistência contra magias adversárias -4 de dano.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Fúria bersek",
            "description": "Aumenta dano em +4 e resistência a efeitos temporariamente, mas fica exausto após 3 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722d")]
            },
            "cost": {
                "mana": 0,
                "energy": 20
            }
        },
        {
            "name": "Movimento Rápido",
            "description": "Aumenta o deslocamento base em +5 na rolagem.",
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
            "description": "Pode desafiar um inimigo, forçando-o a atacar o cavaleiro, recebe -2 de dano desse inimigo.",
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
            "description": "Concede bônus a aliados próximos +2 em todas as rolagens.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722e")]
            },
            "cost": {
                "mana": 0,
                "energy": 7
            }
        },
        {
            "name": "Conjuração Espiritual",
            "description": "Invoca espíritos para assistência em combate ou em feitiços dando +5 em rolagens de ataque.",
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
            },
        },
        {
            "name": "Resistência à Magia",
            "description": "Recebe +2 em testes de resistência contra efeitos mágicos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Fortitude Anã",
            "description": "+2 em testes de Fortitude.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Conhecimento das Rochas",
            "description": "+4 em testes relacionados a rochas e minerais.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Determinação Anã",
            "description": "Recebe +2 em testes de resistência contra efeitos de medo.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Artesão Mestre",
            "description": "+2 em testes para criar ou reparar armas e armaduras.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resistência Infernal",
            "description": "Recebe resistência 10 a fogo.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Magia de Chamas",
            "description": "Pode lançar a magia Bola de Fogo uma vez ao dia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 20,
                "energy": 0
            }
        },
        {
            "name": "Sopro Infernal",
            "description": "Ataque em cone que causa dano de fogo.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 15,
                "energy": 10
            }
        },
        {
            "name": "Resistência Mental",
            "description": "Recebe +2 em testes de Vontade.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Aura Demoníaca",
            "description": "Intimida inimigos próximos, reduzindo a moral deles.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resiliência Humana",
            "description": "Recebe +1 em todos os testes de resistência.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Treinamento Militar",
            "description": "Recebe proficiência com todas as armas simples e marciais.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Habilidade com Idiomas",
            "description": "Pode aprender um idioma adicional.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 0
            }
        },
        {
            "name": "Determinação Humana",
            "description": "Pode re-rolar um teste de Vontade uma vez por dia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Prodígio",
            "description": "Recebe +1 em todas as perícias.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Esquiva Ágil",
            "description": "Recebe +2 em testes de Esquiva.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Rapidez Halfling",
            "description": "Recebe +10 em deslocamento.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Vontade de Ferro",
            "description": "Recebe +2 em testes de Vontade.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Furtividade",
            "description": "Recebe +4 em testes de Furtividade.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resistência a Magia",
            "description": "Recebe +2 em testes de resistência contra magias.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Força Brutal",
            "description": "Recebe +2 em testes de Força.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Carga Poderosa",
            "description": "Pode realizar uma investida causando dano adicional.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Resistência a Sangramento",
            "description": "Recebe +2 em testes de resistência contra sangramentos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Intimidação Natural",
            "description": "Recebe +4 em testes de Intimidação.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Vigor do Minotauro",
            "description": "Regenera 1 ponto de vida por rodada.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Mutação Caótica",
            "description": "Recebe uma mutação benéfica aleatória.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Visão Caótica",
            "description": "Permite ver através de ilusões e disfarces.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 10,
                "energy": 5
            }
        },
        {
            "name": "Corrupção Natural",
            "description": "Causa dano em área contra inimigos ao redor.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 15,
                "energy": 10
            }
        },
        {
            "name": "Resistência ao Medo",
            "description": "Recebe +2 em testes de resistência contra efeitos de medo.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Regeneração Caótica",
            "description": "Recupera 2 pontos de vida por rodada enquanto estiver em combate.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723b")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Força Orc",
            "description": "Recebe +2 em testes de força quando enfurecido.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Resistência Orc",
            "description": "Recebe +2 em testes de fortitude.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Berserker",
            "description": "Aumenta o dano quando com pouca vida.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 15
            }
        },
        {
            "name": "Visão Orc",
            "description": "Recebe visão no escuro de até 24m.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Caçador Implacável",
            "description": "Recebe +4 em testes de rastreamento.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723c")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Mente Brilhante",
            "description": "Recebe +2 em testes de inteligência.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Pequeno Mas Poderoso",
            "description": "Recebe +2 em testes de destreza.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Magia Engenhosa",
            "description": "Pode lançar uma magia de truque adicional por dia.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 5,
                "energy": 0
            }
        },
        {
            "name": "Resiliência Gnômica",
            "description": "Recebe +2 em testes de resistência contra venenos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Visão de Ilusão",
            "description": "Recebe +4 em testes para detectar ilusões.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723d")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Rugido de Batalha",
            "description": "Emite um rugido que aumenta o dano e a velocidade de ataque de todos os aliados próximos por 2 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 15,
                "energy": 10
            }
        },
        {
            "name": "Pele de Pedra",
            "description": "Endurece a pele, reduzindo em 50% o dano físico recebido por 3 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 20,
                "energy": 15
            }
        },
        {
            "name": "Ataque Giratório",
            "description": "Gira em círculo, atingindo todos os inimigos ao redor com dano físico.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 10,
                "energy": 20
            }
        },
        {
            "name": "Murro de Atordoamento",
            "description": "Desfere um golpe poderoso que atordoa o inimigo por 1 rodada.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 5,
                "energy": 15
            }
        },
        {
            "name": "Guardião de Pedra",
            "description": "Invoca uma estátua de pedra que atrai ataques inimigos por 3 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7239")]
            },
            "cost": {
                "mana": 25,
                "energy": 20
            }
        },
        {
            "name": "Chicote de Fogo",
            "description": "Lança um chicote de fogo que causa dano contínuo por 2 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 15,
                "energy": 10
            }
        },
        {
            "name": "Correntes Infernais",
            "description": "Prende o inimigo em correntes de fogo, impedindo movimento por 2 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 20,
                "energy": 15
            }
        },
        {
            "name": "Escudo Infernal",
            "description": "Cria um escudo de fogo ao redor do corpo que reduz o dano recebido e causa dano aos inimigos que o atacarem.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 30,
                "energy": 20
            }
        },
        {
            "name": "Medo Implacável",
            "description": "Faz com que todos os inimigos em um raio de 10 metros fujam em terror por 2 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 25,
                "energy": 15
            }
        },
        {
            "name": "Bola de Fogo",
            "description": "Lança uma bola de fogo que explode ao contato, causando dano em área.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723e")]
            },
            "cost": {
                "mana": 15,
                "energy": 10
            }
        },
        {
            "name": "Ataque Impiedoso",
            "description": "Desfere uma série de golpes rápidos que aumentam a cada acerto bem-sucedido.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 0,
                "energy": 20
            }
        },
        {
            "name": "Vontade Indomável",
            "description": "Aumenta drasticamente a resistência a todos os tipos de controle mental por 3 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 20,
                "energy": 10
            }
        },
        {
            "name": "Golpe Decisivo",
            "description": "Concentra todas as forças em um único golpe devastador.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 10,
                "energy": 15
            }
        },
        {
            "name": "Camuflagem",
            "description": "Fica invisível por 2 rodadas ou até que ataque, ideal para emboscadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 20,
                "energy": 10
            }
        },
        {
            "name": "Presença Inspiradora",
            "description": "Aumenta a moral e eficácia em combate dos aliados próximos por 2 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a7237")]
            },
            "cost": {
                "mana": 10,
                "energy": 10
            }
        },
        {
            "name": "Sorte Halfling",
            "description": "Aumenta a chance de esquiva e acerto crítico por 3 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 10,
                "energy": 10
            }
        },
        {
            "name": "Salto Ágil",
            "description": "Permite ao Halfling realizar um salto extraordinário, escapando de cercos ou alcançando locais elevados.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Manto de Sombra",
            "description": "Fica invisível em áreas de sombra, ideal para emboscadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 15,
                "energy": 5
            }
        },
        {
            "name": "Agilidade Supremar",
            "description": "Aumenta a velocidade de movimento drasticamente por 1 rodada.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723f")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Força Brutal",
            "description": "Recebe um bônus de +2 em testes de Força.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Carga Poderosa",
            "description": "Realiza uma investida que causa dano adicional ao atingir o alvo.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Resistência a Sangramento",
            "description": "Recebe +2 em testes de resistência contra sangramentos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Intimidação Natural",
            "description": "Recebe +4 em testes de Intimidação.",
            "related_to": {
                "race_ids": [ObjectId("66bf65924681d1641b7a723a")]
            },
            "cost": {
                "mana": 0,
                "energy": 5
            }
        },
        {
            "name": "Pacto Sombrio",
            "description": "Recebe poderes através de um pacto com uma entidade poderosa, ganhando +5 em magias sombrias.",
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
            "description": "Aumenta a resistência contra ataques sombrios, tomando -5 de dano.",
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
            "description": "Ganha prioridade de ataque, recebendo +4 na rolagem de Iniciativa.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 15,
                "energy": 0
            }
        },
        {
            "name": "Resistência a Magia",
            "description": "Aumenta a resistência contra magias adversárias, reduzindo o dano em 4 pontos.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722c")]
            },
            "cost": {
                "mana": 0,
                "energy": 10
            }
        },
        {
            "name": "Fúria Berserker",
            "description": "Aumenta o dano em +4 e a resistência a efeitos temporariamente, mas fica exausto após 3 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722d")]
            },
            "cost": {
                "mana": 0,
                "energy": 20
            }
        },
        {
            "name": "Movimento Rápido",
            "description": "Aumenta o deslocamento base, dando +5 na rolagem de movimentação.",
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
            "description": "Força um inimigo a atacá-lo, recebendo -2 de dano desse inimigo.",
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
            "description": "Concede +2 em todas as rolagens para aliados próximos por 2 rodadas.",
            "related_to": {
                "race_ids": [ObjectId("66bf65914681d1641b7a722e")]
            },
            "cost": {
                "mana": 0,
                "energy": 7
            }
        },
        {
            "name": "Conjuração Espiritual",
            "description": "Invoca espíritos que dão +5 em rolagens de ataque para aliados próximos por 2 rodadas.",
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
            "description": "Pode comandar espíritos para realizar uma ação específica, concedendo +2 em uma rolagem escolhida.",
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
            "description": "Forma um vínculo com um espírito que oferece +2 em todas as rolagens por 3 rodadas.",
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
            "description": "Cria uma poção que recupera 10 de vida ou 10 de mana.",
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
            "description": "Cria uma bomba que causa 10 de dano em área.",
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
            "description": "Concede +2 em Força e -2 em Destreza por 3 rodadas.",
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
            "description": "Transforma-se, adquirindo +5 de vida e +2 em todas as rolagens por 3 rodadas.",
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
            "description": "Recupera 5 pontos de vida por rodada enquanto estiver transformado.",
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
            "description": "Melhora a forma transformada, ganhando +3 de vida e +2 de dano adicional por 3 rodadas.",
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
        ability["icon"] = get_icon_for_ability(ability["name"], ability["description"])
        ability.setdefault("system_id", "medieval")

        # The seed data below uses "energy" (English); every resource key
        # elsewhere in the medieval system (character resources, the
        # /use_skill cost check, ...) uses "energia" (see game_systems.py).
        # Normalize here so a skill's mana/energia cost actually matches
        # against the character's resources dict.
        cost = ability.get("cost")
        if cost and "energy" in cost:
            cost["energia"] = cost.pop("energy")

        db.abilities.update_one(
            {"name": ability["name"], "system_id": ability["system_id"]},
            {"$set": ability},
            upsert=True
        )


def get_abilities_by_system(db, system_id):
    return list(db.abilities.find({"system_id": system_id}))


def create_default_abilities_other_systems(db):
    """A modest, freely-selectable ability pool for each non-medieval system."""
    other_abilities = [
        # --- Call of Cthulhu ---
        {"system_id": "cthulhu", "name": "Leitura Rápida", "description": "Absorve o essencial de um texto em uma fração do tempo normal.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 5}},
        {"system_id": "cthulhu", "name": "Nervos de Aço", "description": "Resiste um pouco melhor a visões perturbadoras antes de perder a sanidade.",
         "related_to": {"race_ids": []}, "cost": {"sanidade": 0}},
        {"system_id": "cthulhu", "name": "Golpe de Sorte", "description": "Força um resultado ligeiramente melhor num momento crítico.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 10}},
        {"system_id": "cthulhu", "name": "Memória Eidética", "description": "Recorda detalhes exatos de algo visto ou lido uma única vez.",
         "related_to": {"race_ids": []}, "cost": {"sanidade": 5}},
        {"system_id": "cthulhu", "name": "Faro Investigativo", "description": "Nota uma pista que outros passariam direto.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 5}},
        {"system_id": "cthulhu", "name": "Sangue Frio", "description": "Mantém a compostura por mais um instante diante do inominável.",
         "related_to": {"race_ids": []}, "cost": {"sanidade": 5}},
        {"system_id": "cthulhu", "name": "Contatos na Imprensa", "description": "Consegue informações através de um conhecido jornalista ou editor.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 5}},
        {"system_id": "cthulhu", "name": "Instinto de Sobrevivência", "description": "Pressente o perigo um instante antes que ele se manifeste.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 10}},
        {"system_id": "cthulhu", "name": "Conhecimento Proibido", "description": "Recorda um fragmento de um texto oculto lido há muito tempo — ao custo da própria sanidade.",
         "related_to": {"race_ids": []}, "cost": {"sanidade": 10}},
        {"system_id": "cthulhu", "name": "Mão Firme", "description": "Estabiliza um ferimento grave sob pressão extrema.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 5}},
        {"system_id": "cthulhu", "name": "Vislumbre Além do Véu", "description": "Enxerga por um instante algo que não deveria ser visto — a um custo terrível.",
         "related_to": {"race_ids": []}, "cost": {"sanidade": 15}},
        {"system_id": "cthulhu", "name": "Rede de Informantes", "description": "Tem um contato disposto a compartilhar um segredo por um preço.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 10}},
        {"system_id": "cthulhu", "name": "Determinação Inabalável", "description": "Resiste a um teste de sanidade através de pura força de vontade.",
         "related_to": {"race_ids": []}, "cost": {"sanidade": 0}},
        {"system_id": "cthulhu", "name": "Primeiros Socorros Avançados", "description": "Trata ferimentos graves com o que tiver em mãos.",
         "related_to": {"race_ids": []}, "cost": {"sorte": 5}},

        # --- Western ---
        {"system_id": "western", "name": "Saque Relâmpago", "description": "Desembainha e atira antes que o oponente perceba.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Olho de Águia", "description": "Acerta alvos distantes com precisão incomum.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Fôlego de Ferro", "description": "Continua de pé mesmo gravemente ferido.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 10}},
        {"system_id": "western", "name": "Lábia de Cartola", "description": "Convence quase qualquer um numa negociação de boteco.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Cavaleiro Nato", "description": "Manobra sua montaria com perfeição mesmo em terreno difícil.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Faro para Problemas", "description": "Pressente uma emboscada antes que ela aconteça.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Tiro Certeiro", "description": "Mira com calma para garantir um golpe decisivo.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 10}},
        {"system_id": "western", "name": "Blefe de Aço", "description": "Convence o oponente de que está em desvantagem, mesmo sem estar.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Rastreador Nato", "description": "Segue uma pista antiga que qualquer outro já teria perdido.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Coração de Ferro", "description": "Permanece firme diante de ameaças e intimidação.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Duelista Experiente", "description": "Ganha vantagem no primeiro confronto direto do dia.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 10}},
        {"system_id": "western", "name": "Amigo dos Animais", "description": "Acalma e comanda animais assustados ou hostis.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 5}},
        {"system_id": "western", "name": "Reviravolta na Mesa", "description": "Vira uma negociação a seu favor no último momento.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 10}},
        {"system_id": "western", "name": "Sangue-Frio sob Fogo", "description": "Mantém a pontaria mesmo debaixo de tiroteio intenso.",
         "related_to": {"race_ids": []}, "cost": {"determinacao": 10}},

        # --- Cyberpunk ---
        {"system_id": "cyberpunk", "name": "Overclock Neural", "description": "Acelera reflexos por alguns instantes, à custa de energia cibernética.",
         "related_to": {"race_ids": []}, "cost": {"energia": 15}},
        {"system_id": "cyberpunk", "name": "Invasão Silenciosa", "description": "Invade um sistema sem disparar alarmes.",
         "related_to": {"race_ids": []}, "cost": {"energia": 20}},
        {"system_id": "cyberpunk", "name": "Firewall Mental", "description": "Reforça a mente contra ataques de intrusão neural.",
         "related_to": {"race_ids": []}, "cost": {"humanidade": 5}},
        {"system_id": "cyberpunk", "name": "Braço Cibernético", "description": "Golpe amplificado por um implante mecânico.",
         "related_to": {"race_ids": []}, "cost": {"energia": 10}},
        {"system_id": "cyberpunk", "name": "Camuflagem Óptica", "description": "Um implante dobra a luz ao redor do usuário por um instante.",
         "related_to": {"race_ids": []}, "cost": {"energia": 20}},
        {"system_id": "cyberpunk", "name": "Âncora Humana", "description": "Resiste à erosão da própria humanidade num momento crítico.",
         "related_to": {"race_ids": []}, "cost": {"humanidade": 0}},
        {"system_id": "cyberpunk", "name": "Reflexos Sintéticos", "description": "Implantes neurais aceleram uma esquiva quase impossível.",
         "related_to": {"race_ids": []}, "cost": {"energia": 15}},
        {"system_id": "cyberpunk", "name": "Quebra de Criptografia", "description": "Força a entrada em um sistema fortemente protegido.",
         "related_to": {"race_ids": []}, "cost": {"energia": 25}},
        {"system_id": "cyberpunk", "name": "Contato na Rede", "description": "Um fixer ou informante paga uma dívida antiga na hora certa.",
         "related_to": {"race_ids": []}, "cost": {"humanidade": 5}},
        {"system_id": "cyberpunk", "name": "Adrenalina Sintética", "description": "Um implante libera estimulantes que ignoram a dor por um instante.",
         "related_to": {"race_ids": []}, "cost": {"energia": 15}},
        {"system_id": "cyberpunk", "name": "Rastreamento Digital", "description": "Localiza um alvo através de suas pegadas digitais.",
         "related_to": {"race_ids": []}, "cost": {"energia": 15}},
        {"system_id": "cyberpunk", "name": "Encanto Corporativo", "description": "Usa etiqueta e status para abrir portas fechadas para os outros.",
         "related_to": {"race_ids": []}, "cost": {"humanidade": 5}},
        {"system_id": "cyberpunk", "name": "Redundância Neural", "description": "Um backup mental reduz o dano de um ataque de intrusão neural.",
         "related_to": {"race_ids": []}, "cost": {"energia": 20}},
        {"system_id": "cyberpunk", "name": "Faro de Fixer", "description": "Sempre sabe onde conseguir algo — por um preço.",
         "related_to": {"race_ids": []}, "cost": {"humanidade": 0}},
        {"system_id": "cyberpunk", "name": "Overdrive Muscular", "description": "Implantes musculares entregam um golpe muito acima do normal.",
         "related_to": {"race_ids": []}, "cost": {"energia": 20}},
    ]

    for ability in other_abilities:
        ability["icon"] = None
        db.abilities.update_one(
            {"name": ability["name"], "system_id": ability["system_id"]},
            {"$set": ability},
            upsert=True,
        )


def get_icon_for_ability(ability_name, ability_description):
    icon_map = {
        "visão": "visao_noturna.png",
        "luz": "bola_energia_azul.png",
        "frio": "flechas_gelo.png",
        "eletricidade": "raio_choque.png",
        "percepção": "percepcao_avancada.png",
        "magia": "magia_trevas.png",
        "fogo": "bola_fogo.png",
        "caos": "mutacao_caotica.png",
        "chifres": "chifrada_touro.png",
        "intimidação": "intimidacao_natural.png",
        "esquiva": "esquiva_agil.png",
        "força": "forca.png",
        "cura": "cura_magia_3.png",
        "espírito": "conjuracao_espiritual.png",
        "trevas": "pilar_trevas.png",
        "raio": "raio_luz.png",
        "explosão": "explosao_luz.png",
        "invisível": "camuflagem.png",
        "berserker": "furia_bersek.png",
        "veneno": "bola_veneno.png",
        "teleporte": "teleporte_efeito.png",
        "armas": "maestria_em_armas.png",
        "transformação": "transformacao.png",
        "alucinação": "alucinacao.png",
        "aprisionar alma": "aprizionar_alma.png",
        "arremesso pessoa": "arremeco_pessoa.png",
        "assassino furtivo": "assasino_furtivo.png",
        "ataque espada": "ataque_espada.png",
        "ataque estrela": "ataque_estrela.png",
        "ataque flor": "ataque_flor.png",
        "ataque natureza": "ataque_naturesa.png",
        "ataque natureza 2": "ataque_naturesa_2.png",
        "barreira": "barreira_efeito.png",
        "neve": "bolas_neve.png",
        "bola arcana": "bola_arcana.png",
        "energia": "bola_energia.png",
        "bola energia azul": "bola_energia_azul.png",
        "bola energia roxa": "bola_energia_roxa.png",
        "bola fogo": "bola_fogo.png",
        "bola veneno": "bola_veneno.png",
        "bolha": "bolha_agua.png",
        "buff": "buff_efeito.png",
        "buff espada": "buff_espada.png",
        "buff roxo": "buff_roxo_area.png",
        "flechas": "chuva_flechas.png",
        "chuva de meteoros": "chuva_meteoros_azul.png",
        "clarevidência": "clarevidencia_efeito.png",
        "conhecimento": "conhecimento_magia.png",
        "corte duplo": "corte_duplo.png",
        "corte espada": "corte_espada.png",
        "curar": "cura_magia_3.png",
        "cura poderosa": "cura_area_poderosa.png",
        "cura natureza": "cura_naturesa.png",
        "dardo prata": "dardo_prata.png",
        "dardo prata 2": "dardo_prata2.png",
        "death": "death_efeito.png",
        "defesa": "defesa_efeito.png",
        "desaparecer": "desaparecer.png",
        "disparo arcano": "disparo_arcano_forte.png",
        "efeito rage": "efeito_rage.png",
        "efeito ragnarok": "efeito_ragnarok.png",
        "efeito veneno": "efeito_veneno.png",
        "eletricidade": "eletrecidade_efeito.png",
        "escudo": "escudo_defesa.png",
        "escudo defesa": "escudo_defesa_2.png",
        "escudo mágico": "escudo_magico.png",
        "espada divina": "espada_divina.png",
        "exaustão": "exaustao_efeito.png",
        "explosão trevas": "explosao_trevas.png",
        "explosão luz": "explosao_luz.png",
        "fênix": "fenix.png",
        "flechada": "flechada.png",
        "flechas gelo": "flechas_gelo.png",
        "flechas triplas": "flechas_triplas.png",
        "forja": "forja_martelo.png",
        "fúria": "furia_2.png",
        "fúria troll": "furia_troll.png",
        "golpe água": "golpe_agua.png",
        "golpe energia": "golpe_energia.png",
        "golpe garras": "golpe_garras_forca.png",
        "granada": "granada.png",
        "incendiar": "icendiar_efeito.png",
        "inimigo congelado": "inimigo_congelado.png",
        "labareda fogo": "labareda_fogo.png",
        "lâmina arremessável": "lamina_arremessavel.png",
        "lança": "lanca.png",
        "lanças": "lancas.png",
        "magia amarela": "magia_amarela.png",
        "magia gelo": "magia_gelo.png",
        "magia morte": "magia_morte.png",
        "maldicao": "maldicao_efeito.png",
        "mana": "mana_efeito.png",
        "mão cura": "mao_cura.png",
        "meditação": "meditacao.png",
        "minotauro resistência": "minotauro_resistencia.png",
        "mordida": "mordida_monstro.png",
        "mordida urso": "mordida_urso.png",
        "multiplas bolas de fogo": "multiplas_bolas_fogo.png",
        "noite lua": "noite_lua_efeito.png",
        "onda roxa": "onda_roxa.png",
        "paixão": "paixao_efeito.png",
        "parede de gelo": "parede_gelo.png",
        "asas": "par_asas.png",
        "pilar energia arcana": "pilar_energia_arcana.png",
        "pilar fogo": "pilar_fogo.png",
        "pilar gelo": "pilar_gelo.png",
        "poder tempestade": "poder_tempestade.png",
        "purificar": "purificar_efeito.png",
        "raios": "raios.png",
        "raio arcano": "raio_arcano.png",
        "raio choque": "raio_choque.png",
        "raio duplo roxo": "raio_duplo_roxo.png",
        "raio energia azul": "raio_energia_azul.png",
        "raio luz purificadora": "raio_luz_purificadora.png",
        "raio roxo": "raio_roxo.png",
        "raio trevas": "raio_trevas.png",
        "raio venenoso": "raio_venenoso.png",
        "runa roxa": "runa_roxa.png",
        "sabedoria": "sabedoria.png",
        "silêncio": "silencio_efeito.png",
        "sorte": "sorte_efeito.png",
        "super onda água": "super_onda_agua.png",
        "super raios": "super_raios.png",
        "super raio luz purificadora": "super_raio_luz_purificadora.png",
        "super soco": "super_soco.png",
        "tartaruga": "tartaruga.png",
        "teia de aranha": "teia_aranha.png",
        "teleporte": "teleporte_efeito.png",
        "tempestade glacial": "tempestade_glacial.png",
        "tempo": "tempo_efeito.png",
        "tigre": "tigre.png",
        "tiro": "tiro.png",
        "velocidade": "velocidade_efeito.png",
        "veneno roxo": "veneno_roxo.png"
    }

    # Search for keywords in the name or description to assign an icon
    for keyword, icon in icon_map.items():
        if keyword in ability_name.lower() or keyword in ability_description.lower():
            return icon

    # Default icon if no specific match is found
    return "default_icon.png"


def get_ability_by_id(db, ability_id):
    return db.abilities.find_one({"_id": ObjectId(ability_id)})
