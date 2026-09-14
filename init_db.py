from conection_db import connection
from models.abilities_model import (create_default_abilities,
                                    create_default_abilities_other_systems)
from models.class_model import (create_default_classes,
                                create_default_classes_other_systems)
from models.enemies_model import (create_default_enemies,
                                  create_default_enemies_other_systems)
from models.race_model import create_default_races

db = connection()

create_default_classes(db)
create_default_classes_other_systems(db)
create_default_races(db)
create_default_abilities(db)
create_default_abilities_other_systems(db)
create_default_enemies(db)
create_default_enemies_other_systems(db)

print("Banco de dados inicializado: classes, raças, habilidades e inimigos para todos os sistemas.")
