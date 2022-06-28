import logging

import flask

from arboretum import models

blueprint = flask.Blueprint("rest", __name__)

LOGGER = logging.getLogger(__name__)
CONTENT_TYPE_HEADER_JSON_UTF_8 = {"Content-Type": "application/json, charset=utf-8"}


@blueprint.get("/plants")
def get_plants():
    plants = models.Plant.query.filter_by(**flask.request.args).all()
    plant_schema = models.PlantSchema(many=True)
    plants_json = plant_schema.dumps(plants)
    return plants_json, 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@blueprint.get("/plants/<int:plant_id>")
def get_plant_by_id(plant_id):
    plant = models.Plant.query.get(plant_id)
    plant_schema = models.PlantSchema()
    plant_json = plant_schema.dumps(plant)
    return plant_json, 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@blueprint.post("/plants")
def add_plant():
    payload = flask.request.json
    plant_schema = models.PlantSchema()
    plant = plant_schema.load(payload)
    models.db.session.add(plant)
    models.db.session.commit()
    LOGGER.info(f"Created record: {plant}")
    return plant_schema.dumps(plant), 201, CONTENT_TYPE_HEADER_JSON_UTF_8


@blueprint.delete("/plants/<_id>")
def delete_plant(_id):
    plant_to_delete = models.Plant.query.filter_by(id=_id).first()
    models.db.session.delete(plant_to_delete)
    models.db.session.commit()
    LOGGER.info(f"Deleted record: {plant_to_delete}")
    response_body = {"message": f"Plant (id: {_id}, name: {plant_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@blueprint.get("/plant-families")
def get_plant_families():
    families = models.PlantFamily.query.filter_by(**flask.request.args).all()
    family_schema = models.PlantFamilySchema(many=True)
    return family_schema.dumps(families), 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@blueprint.post("/plant-families")
def add_plant_family():
    payload = flask.request.json
    plant_family_schema = models.PlantFamilySchema()
    plant_family = plant_family_schema.load(payload)
    models.db.session.add(plant_family)
    models.db.session.commit()
    return plant_family_schema.dumps(plant_family), 201, CONTENT_TYPE_HEADER_JSON_UTF_8


@blueprint.delete("/plant-family/<_id>")
def delete_plant_family(_id):
    family_to_delete = models.PlantFamily.query.filter_by(id=_id).first()
    models.db.session.delete(family_to_delete)
    models.db.session.commit()
    LOGGER.info(f"Deleted record: {family_to_delete}")
    response_body = {"message": f"Plant family (id: {_id}, name: {family_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@blueprint.get("/life-forms")
def get_life_forms():
    life_forms = models.PlantLifeForm.query.filter_by(**flask.request.args).all()
    life_form_schema = models.PlantLifeFormSchema(many=True)
    return life_form_schema.dumps(life_forms), 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@blueprint.get("/weed-categories")
def get_weed_categories():
    categories = models.WeedCategory.query.filter_by(**flask.request.args).all()
    category_schema = models.WeedCategorySchema(many=True)
    return category_schema.dumps(categories), 200, CONTENT_TYPE_HEADER_JSON_UTF_8
