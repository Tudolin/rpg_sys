from conection_db import connection
from models.abilities_model import create_default_abilities
from models.class_model import create_default_classes
from models.race_model import create_default_races

create_default_classes(connection('classes'))
create_default_races(connection('races'))
# create_default_abilities(connection('abilities'))
print("Banco de dados inicializado com classes e raças padrão.")
