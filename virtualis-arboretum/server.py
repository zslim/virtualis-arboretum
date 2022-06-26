import logging

import flask
from marshmallow import exceptions
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc
from swagger_gen.lib.wrappers import swagger_metadata

import app_init
import models
import util
from app_init import app, db

LOGGER = logging.getLogger(__name__)


@swagger_metadata(summary="Get all plants")
@app.route("/plant", methods=["GET"])
def get_plants():
    plants = models.Plant.query.all()
    plant_schema = models.PlantSchema(many=True)
    plants_json = plant_schema.dumps(plants)
    return plants_json, 200, {"Content-Type": "application/json, charset=utf-8"}


@app.route("/plant", methods=["POST"])
@swagger_metadata(
    summary="Add new plant",
    request_model=util.get_schema_meta(models.PlantSchema),
    response_model=[(201, "Created"), (400, "Bad request"), (404, "Resource not found")]
)
def add_plant():
    payload = flask.request.json
    plant_schema = models.PlantSchema()
    plant = plant_schema.load(payload)
    db.session.add(plant)
    db.session.commit()
    LOGGER.info(f"Created record: {plant}")
    return plant_schema.dumps(plant), 201, {"Content-Type": "application/json, charset=utf-8"}


@app.route("/plant/<_id>", methods=["DELETE"])
@swagger_metadata(query_params=[])
def delete_plant(_id):
    plant_to_delete = models.Plant.query.filter_by(id=_id).first()
    db.session.delete(plant_to_delete)
    db.session.commit()
    LOGGER.info(f"Deleted record: {plant_to_delete}")
    response_body = {"message": f"Plant (id: {_id}, name: {plant_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@app.route("/plant-family", methods=["GET"])
def get_plant_families():
    families = models.PlantFamily.query.all()
    family_schema = models.PlantFamilySchema(many=True)
    return family_schema.dumps(families), 200, {"Content-Type": "application/json, charset=utf-8"}


@app.route("/plant-family", methods=["POST"])
@swagger_metadata(
    summary="Add plant family",
    request_model=util.get_schema_meta(models.PlantFamilySchema),
    response_model=[(201, "Created"), (400, "Bad request")]
)
def add_plant_family():
    payload = flask.request.json
    plant_family_schema = models.PlantFamilySchema()
    plant_family = plant_family_schema.load(payload)
    db.session.add(plant_family)
    db.session.commit()
    return plant_family_schema.dumps(plant_family), 201, {"Content-Type": "application/json, charset=utf-8"}


@app.route("/plant-family/<_id>", methods=["DELETE"])
@swagger_metadata(query_params=[])
def delete_plant_family(_id):
    family_to_delete = models.PlantFamily.query.filter_by(id=_id).first()
    db.session.delete(family_to_delete)
    db.session.commit()
    LOGGER.info(f"Deleted record: {family_to_delete}")
    response_body = {"message": f"Plant family (id: {_id}, name: {family_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@app.route("/life-form", methods=["GET"])
def get_life_forms():
    life_forms = models.PlantLifeForm.query.all()
    life_form_schema = models.PlantLifeFormSchema(many=True)
    return life_form_schema.dumps(life_forms), 200, {"Content-Type": "application/json, charset=utf-8"}


@app.route("/weed-category", methods=["GET"])
def get_weed_categories():
    categories = models.WeedCategory.query.all()
    category_schema = models.WeedCategorySchema(many=True)
    return category_schema.dumps(categories), 200, {"Content-Type": "application/json, charset=utf-8"}


@app.errorhandler(orm_exc.UnmappedInstanceError)
def handle_unmapped_instance(error):
    response_body = util.create_error_message("referenced resource could not be found", error)
    return response_body, 404, {"Content-Type": "application/json, charset=utf-8"}


@app.errorhandler(exceptions.ValidationError)
def handle_validation_error(error):
    response_body = util.create_error_message("input could not be validated", error)
    return response_body, 400, {"Content-Type": "application/json, charset=utf-8"}


@app.errorhandler(exc.IntegrityError)
def handle_integrity_error(error):
    response_body = util.create_error_message("constraint violation", error)
    return response_body, 400, {"Content-Type": "application/json, charset=utf-8"}


@app.errorhandler(exc.DataError)
def handle_data_error(error):
    response_body = util.create_error_message("invalid input", error)
    return response_body, 400, {"Content-Type": "application/json, charset=utf-8"}


# Need to configure Swagger after url definitions
swagger = app_init.init_swagger(app)
swagger.configure()


if __name__ == '__main__':
    app.run()
