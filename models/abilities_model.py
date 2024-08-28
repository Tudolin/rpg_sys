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
