import logging

import flask
from marshmallow import exceptions
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc

from arboretum import app_init
from arboretum import models
from arboretum import util
from arboretum.app_init import app, db

LOGGER = logging.getLogger(__name__)
CONTENT_TYPE_HEADER_JSON_UTF_8 = {"Content-Type": "application/json, charset=utf-8"}


@app.route("/plants", methods=["GET"])
def get_plants():
    plants = models.Plant.query.filter_by(**flask.request.args).all()
    plant_schema = models.PlantSchema(many=True)
    plants_json = plant_schema.dumps(plants)
    return plants_json, 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/plants/<int:plant_id>", methods=["GET"])
def get_plant_by_id(plant_id):
    plant = models.Plant.query.get(plant_id)
    plant_schema = models.PlantSchema()
    plant_json = plant_schema.dumps(plant)
    return plant_json, 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/plants", methods=["POST"])
def add_plant():
    payload = flask.request.json
    plant_schema = models.PlantSchema()
    plant = plant_schema.load(payload)
    db.session.add(plant)
    db.session.commit()
    LOGGER.info(f"Created record: {plant}")
    return plant_schema.dumps(plant), 201, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/plants/<_id>", methods=["DELETE"])
def delete_plant(_id):
    plant_to_delete = models.Plant.query.filter_by(id=_id).first()
    db.session.delete(plant_to_delete)
    db.session.commit()
    LOGGER.info(f"Deleted record: {plant_to_delete}")
    response_body = {"message": f"Plant (id: {_id}, name: {plant_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@app.route("/plant-families", methods=["GET"])
def get_plant_families():
    families = models.PlantFamily.query.filter_by(**flask.request.args).all()
    family_schema = models.PlantFamilySchema(many=True)
    return family_schema.dumps(families), 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/plant-families", methods=["POST"])
def add_plant_family():
    payload = flask.request.json
    plant_family_schema = models.PlantFamilySchema()
    plant_family = plant_family_schema.load(payload)
    db.session.add(plant_family)
    db.session.commit()
    return plant_family_schema.dumps(plant_family), 201, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/plant-family/<_id>", methods=["DELETE"])
def delete_plant_family(_id):
    family_to_delete = models.PlantFamily.query.filter_by(id=_id).first()
    db.session.delete(family_to_delete)
    db.session.commit()
    LOGGER.info(f"Deleted record: {family_to_delete}")
    response_body = {"message": f"Plant family (id: {_id}, name: {family_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@app.route("/life-forms", methods=["GET"])
def get_life_forms():
    life_forms = models.PlantLifeForm.query.filter_by(**flask.request.args).all()
    life_form_schema = models.PlantLifeFormSchema(many=True)
    return life_form_schema.dumps(life_forms), 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/weed-categories", methods=["GET"])
def get_weed_categories():
    categories = models.WeedCategory.query.filter_by(**flask.request.args).all()
    category_schema = models.WeedCategorySchema(many=True)
    return category_schema.dumps(categories), 200, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.route("/swagger/swagger.json", methods=["GET"])
def get_swagger_specification():
    swagger_json = util.read_api_spec()
    return flask.jsonify(swagger_json), 200


@app.route("/swagger", methods=["GET"])
def render_swagger_ui():
    return flask.render_template("swagger-index.html")


@app.errorhandler(orm_exc.UnmappedInstanceError)
def handle_unmapped_instance(error):
    response_body = util.create_error_message("referenced resource could not be found", error)
    return response_body, 404, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.errorhandler(exceptions.ValidationError)
def handle_validation_error(error):
    response_body = util.create_error_message("input could not be validated", error)
    return response_body, 400, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.errorhandler(exc.IntegrityError)
def handle_integrity_error(error):
    response_body = util.create_error_message("constraint violation", error)
    return response_body, 400, CONTENT_TYPE_HEADER_JSON_UTF_8


@app.errorhandler(exc.DataError)
def handle_data_error(error):
    response_body = util.create_error_message("invalid input", error)
    return response_body, 400, CONTENT_TYPE_HEADER_JSON_UTF_8


if __name__ == '__main__':
    app.run(
        host=app_init.HOST,
        port=app_init.PORT,
        debug=True
    )
