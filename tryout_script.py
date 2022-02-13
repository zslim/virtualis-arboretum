from models import *


# Életformák betöltése
life_form_path = "init_data_json/life_forms.json"

with open(life_form_path) as f:
    life_form_string = f.read()

life_form_schema = PlantLifeFormSchema(many=True)
life_forms = life_form_schema.loads(life_form_string)


# Családok betöltése
family_path = "init_data_json/families.json"

with open(family_path) as f:
    family_string = f.read()

family_schema = PlantFamilySchema(many=True)
families = family_schema.loads(family_string)


# Növények betöltése
plant_path = "init_data_json/plants.json"

with open(plant_path) as f:
    plant_string = f.read()

plant_schema = PlantSchema(many=True)
plants = plant_schema.loads(plant_string)
