from conection_db import connection
from models.class_model import create_default_classes
from models.race_model import create_default_races

create_default_classes(connection('classes'))
create_default_races(connection('races'))
print("Banco de dados inicializado com classes e raças padrão.")
