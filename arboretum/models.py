from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import post_load
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()
ma = Marshmallow()


class PlantLifeForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(255), unique=True, nullable=False)
    hungarian_name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    location_of_bud = db.Column(db.String(255))
    plants = db.relationship("Plant")
    weed_categories = db.relationship("WeedCategory")


class WeedCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    life_form_id = db.Column(db.Integer, db.ForeignKey("plant_life_form.id"))
    description = db.Column(db.String(255), nullable=False)
    plants = db.relationship("Plant")


class PlantFamily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(255), unique=True, nullable=False)
    hungarian_name = db.Column(db.String(255), nullable=False)
    plants = db.relationship("Plant")


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(255), unique=True, nullable=False)
    hungarian_names = db.Column(postgresql.ARRAY(db.String, dimensions=1), nullable=False)
    division = db.Column(db.String(255))
    class_taxon = db.Column(db.String(255))
    family_id = db.Column(db.Integer, db.ForeignKey("plant_family.id"))
    life_form_id = db.Column(db.Integer, db.ForeignKey("plant_life_form.id"))
    weed_category_id = db.Column(db.Integer, db.ForeignKey("weed_category.id"))
    time_of_blooming = db.Column(db.String(255))
    time_of_ripening = db.Column(db.String(255))
    time_of_germination = db.Column(db.String(255))
    natural_habitat = db.Column(db.String(255))
    light_preference = db.Column(db.String(255))
    humidity_preference = db.Column(db.String(255))
    preferred_soil = db.Column(db.String(255))
    frost_tolerance = db.Column(db.String(255))
    height = db.Column(db.String(255))
    leaf_description = db.Column(db.String(255))
    flower_description = db.Column(db.String(255))
    fruit_description = db.Column(db.String(255))
    description_other = db.Column(db.String(1023))
    image_links = db.Column(postgresql.ARRAY(db.String, dimensions=1))
    decorative_value = db.Column(db.String(255))
    pruning = db.Column(db.String(255))
    pests = db.Column(db.String(255))
    usage = db.Column(db.String(255))
    toxicity = db.Column(db.String(255))
    propagation = db.Column(db.String(255))
    distance_of_lines = db.Column(db.String(255))
    distance_of_plants = db.Column(db.String(255))
    ecological_function = db.Column(db.String(255))
    gardening_function = db.Column(db.String(255))


class BaseSchema(ma.SQLAlchemyAutoSchema):
    @post_load
    def create_object(self, data, **kwargs):
        return self.Meta.model(**data)


class PlantLifeFormSchema(BaseSchema):
    class Meta:
        model = PlantLifeForm


class WeedCategorySchema(BaseSchema):
    class Meta:
        model = WeedCategory
        include_fk = True


class PlantFamilySchema(BaseSchema):
    class Meta:
        model = PlantFamily


class PlantSchema(BaseSchema):
    class Meta:
        model = Plant
        include_fk = True
