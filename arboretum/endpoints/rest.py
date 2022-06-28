import flask

from arboretum import models, data_manager

blueprint = flask.Blueprint("rest", __name__)


@blueprint.get("/plants")
def get_plants():
    plants = models.Plant.query.filter_by(**flask.request.args).all()
    plant_schema = models.PlantSchema(many=True)
    return plant_schema.jsonify(plants), 200


@blueprint.get("/plants/<int:plant_id>")
def get_plant_by_id(plant_id):
    plant = models.Plant.query.get(plant_id)
    plant_schema = models.PlantSchema()
    return plant_schema.jsonify(plant), 200


@blueprint.post("/plants")
def add_plant():
    payload = flask.request.json
    response = data_manager.insert_row(models.PlantSchema, payload)
    return response, 201


@blueprint.delete("/plants/<plant_id>")
def delete_plant(plant_id):
    response_body = data_manager.delete_row(models.Plant, plant_id)
    return flask.jsonify(response_body), 200


@blueprint.get("/plant-families")
def get_plant_families():
    families = models.PlantFamily.query.filter_by(**flask.request.args).all()
    family_schema = models.PlantFamilySchema(many=True)
    return family_schema.jsonify(families), 200


@blueprint.post("/plant-families")
def add_plant_family():
    payload = flask.request.json
    response = data_manager.insert_row(models.PlantFamilySchema, payload)
    return response, 201


@blueprint.delete("/plant-families/<family_id>")
def delete_plant_family(family_id):
    response_body = data_manager.delete_row(models.PlantFamily, family_id)
    return flask.jsonify(response_body), 200


@blueprint.get("/life-forms")
def get_life_forms():
    life_forms = models.PlantLifeForm.query.filter_by(**flask.request.args).all()
    life_form_schema = models.PlantLifeFormSchema(many=True)
    return life_form_schema.jsonify(life_forms), 200


@blueprint.get("/weed-categories")
def get_weed_categories():
    categories = models.WeedCategory.query.filter_by(**flask.request.args).all()
    category_schema = models.WeedCategorySchema(many=True)
    return category_schema.jsonify(categories), 200
