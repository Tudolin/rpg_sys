from bson import ObjectId


def create_default_enemies(db):
    enemies = [
        {
            "name": "Goblin",
            "hp": 10,
            "ataque": 7,
            "defesa": 3,
            "mana": 10,
            "energia": 15,
            "current_hp": 10,
            "resumo": "Criaturas pequenas e traiçoeiras, conhecidas por sua astúcia e velocidade. Goblins tendem a atacar em grupos e são especialistas em emboscadas."
        },
        {
            "name": "Orc",
            "hp": 20,
            "ataque": 12,
            "defesa": 5,
            "mana": 5,
            "energia": 20,
            "current_hp": 20,
            "resumo": "Orcs são guerreiros brutais que confiam em sua força física para dominar seus inimigos. Eles são conhecidos por seu temperamento explosivo e força implacável."
        },
        {
            "name": "Troll",
            "hp": 30,
            "ataque": 15,
            "defesa": 8,
            "mana": 0,
            "energia": 30,
            "current_hp": 30,
            "resumo": "Trolls são criaturas enormes com uma capacidade de regeneração impressionante. Eles são difíceis de derrotar devido à sua resistência e força bruta."
        },
        {
            "name": "Dragão",
            "hp": 150,
            "ataque": 25,
            "defesa": 20,
            "mana": 100,
            "energia": 50,
            "current_hp": 150,
            "resumo": "Dragões são seres lendários com poder avassalador. Eles podem devastar cidades inteiras com seu sopro de fogo e são adversários formidáveis para qualquer aventureiro."
        },
        {
            "name": "Esqueleto",
            "hp": 15,
            "ataque": 10,
            "defesa": 4,
            "mana": 0,
            "energia": 10,
            "current_hp": 15,
            "resumo": "Essas criaturas mortas-vivas são frequentemente encontradas em masmorras antigas. Seus ataques são lentos, mas implacáveis."
        },
        {
            "name": "Lich",
            "hp": 40,
            "ataque": 15,
            "defesa": 10,
            "mana": 200,
            "energia": 40,
            "current_hp": 40,
            "resumo": "Um Lich é um poderoso necromante que alcançou a imortalidade. Suas habilidades mágicas são imensas, e ele comanda exércitos de mortos-vivos."
        },
        {
            "name": "Kobold",
            "hp": 8,
            "ataque": 6,
            "defesa": 2,
            "mana": 5,
            "energia": 10,
            "current_hp": 8,
            "resumo": "Kobolds são pequenos répteis humanoides que vivem em cavernas e minas. Eles são fracos individualmente, mas podem ser perigosos em grande número."
        },
        {
            "name": "Elemental de Fogo",
            "hp": 25,
            "ataque": 18,
            "defesa": 8,
            "mana": 50,
            "energia": 30,
            "current_hp": 25,
            "resumo": "Criaturas compostas de chamas puras, os Elementais de Fogo são resistentes ao fogo e podem incinerar seus inimigos com facilidade."
        },
        {
            "name": "Mímico",
            "hp": 20,
            "ataque": 12,
            "defesa": 10,
            "mana": 0,
            "energia": 25,
            "current_hp": 20,
            "resumo": "Mímicos são criaturas capazes de se disfarçar como objetos inanimados, como baús de tesouro. Eles atacam os desavisados com mordidas poderosas."
        },
        {
            "name": "Demônio",
            "hp": 50,
            "ataque": 20,
            "defesa": 15,
            "mana": 80,
            "energia": 50,
            "current_hp": 50,
            "resumo": "Demônios são seres malévolos originários dos planos infernais. Eles possuem grande poder mágico e físico, sendo adversários terríveis em combate."
        },
        {
            "name": "Aranha Gigante",
            "hp": 18,
            "ataque": 14,
            "defesa": 8,
            "mana": 0,
            "energia": 20,
            "current_hp": 18,
            "resumo": "Aranhas gigantes são predadores mortais que atacam com mordidas venenosas. Elas costumam emboscar suas presas, imobilizando-as com teias pegajosas."
        },
        {
            "name": "Zumbi",
            "hp": 20,
            "ataque": 8,
            "defesa": 5,
            "mana": 0,
            "energia": 20,
            "current_hp": 20,
            "resumo": "Zumbis são mortos-vivos reanimados por magia necromântica. Embora lentos, são incansáveis e atacam seus inimigos até que sejam destruídos."
        },
        {
            "name": "Hidra",
            "hp": 60,
            "ataque": 20,
            "defesa": 15,
            "mana": 10,
            "energia": 40,
            "current_hp": 60,
            "resumo": "A Hidra é uma criatura multi-cabeças que regenera rapidamente suas feridas. Cada vez que uma cabeça é cortada, outras duas nascem em seu lugar."
        },
        {
            "name": "Golem de Pedra",
            "hp": 80,
            "ataque": 18,
            "defesa": 25,
            "mana": 0,
            "energia": 30,
            "current_hp": 80,
            "resumo": "Feito de pedra sólida, o Golem é quase impenetrável. Sua força imensa e resistência tornam-no um adversário formidável."
        },
        {
            "name": "Banshee",
            "hp": 30,
            "ataque": 12,
            "defesa": 10,
            "mana": 100,
            "energia": 25,
            "current_hp": 30,
            "resumo": "Espíritos vingativos que emitem gritos aterrorizantes. A Banshee é capaz de drenar a vida de seus inimigos com seu lamento mortal."
        },
        {
            "name": "Gnoll",
            "hp": 25,
            "ataque": 14,
            "defesa": 8,
            "mana": 0,
            "energia": 20,
            "current_hp": 25,
            "resumo": "Gnolls são criaturas híbridas entre humanos e hienas. São caçadores cruéis e violentos, conhecidos por sua ferocidade em combate."
        },
        {
            "name": "Lobo Dire",
            "hp": 28,
            "ataque": 16,
            "defesa": 9,
            "mana": 0,
            "energia": 25,
            "current_hp": 28,
            "resumo": "Lobos Dire são versões maiores e mais ferozes dos lobos comuns. Eles atacam em matilhas, rasgando suas presas com mandíbulas poderosas."
        },
        {
            "name": "Vampiro",
            "hp": 60,
            "ataque": 18,
            "defesa": 15,
            "mana": 50,
            "energia": 40,
            "current_hp": 60,
            "resumo": "Vampiros são mortos-vivos elegantes e perigosos que se alimentam de sangue. Eles possuem poderes mágicos e são extremamente difíceis de matar."
        },
        {
            "name": "Medusa",
            "hp": 35,
            "ataque": 15,
            "defesa": 12,
            "mana": 30,
            "energia": 25,
            "current_hp": 35,
            "resumo": "Medusas são criaturas monstruosas com o poder de transformar qualquer ser em pedra com seu olhar. São astutas e perigosas em combate."
        },
        {
            "name": "Mantícora",
            "hp": 55,
            "ataque": 20,
            "defesa": 13,
            "mana": 10,
            "energia": 35,
            "current_hp": 55,
            "resumo": "Mantícoras são criaturas ferozes com corpo de leão, asas de morcego e cauda de escorpião. Elas são conhecidas por sua ferocidade e habilidade de voar."
        }
    ]
    
    for enemy_data in enemies:
        enemy_data["spawn_som"] = format_sound_name(enemy_data["name"])  
        enemy_data["img_url"] = get_icon_for_enemy(enemy_data["name"])
        db.enemies.update_one(
            {"name": enemy_data["name"]},
            {"$set": enemy_data},
            upsert=True
        )

def remove_accents(text):
    accents_map = str.maketrans(
        "áàâãäéèêëíìîïóòôõöúùûüçÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ",
        "aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC"
    )
    return text.translate(accents_map)

def format_sound_name(monster_name):
    monster_name_no_accents = remove_accents(monster_name)
    monster_sound_name = monster_name_no_accents.lower().replace(' ', '_')
    return f"{monster_sound_name}.mp3"

def get_icon_for_enemy(monster_name):
    # Remover acentos
    monster_name_no_accents = remove_accents(monster_name)
    monster_icon_name = monster_name_no_accents.lower().replace(' ', '_')
    
    return f"{monster_icon_name}.png"


def enemy_by_id(db, enemy_id):
    return db.enemies.find_one({"_id": ObjectId(enemy_id)})
