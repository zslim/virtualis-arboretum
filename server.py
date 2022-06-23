import logging

import flask
from marshmallow import exceptions
from marshmallow_jsonschema import JSONSchema
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc
from swagger_gen.lib.wrappers import swagger_metadata
from swagger_gen import swagger

import models
import util
from app_init import app, db

LOGGER = logging.getLogger(__name__)
JSON_SCHEMA = JSONSchema()


@swagger_metadata(summary="Get all plants")  # TODO: response encoding & formatting
@app.route("/plant", methods=["GET"])
def get_plants():
    plants = models.Plant.query.all()
    plant_schema = models.PlantSchema(many=True)
    plants_json = plant_schema.dumps(plants)
    return plants_json, 200


@app.route("/plant", methods=["POST"])
@swagger_metadata(
    summary="Add new plant",
    request_model=JSON_SCHEMA.dump(models.PlantSchema())["definitions"]['PlantSchema']['properties'],
    response_model=[(201, "Created"), (400, "Bad request"), (404, "Resource not found")]
)
def add_plant():
    payload = flask.request.json
    plant_schema = models.PlantSchema()
    plant = plant_schema.load(payload)
    db.session.add(plant)
    db.session.commit()
    LOGGER.info(f"Created record: {plant}")
    return plant_schema.dumps(plant), 201


@app.route("/plant/<_id>", methods=["DELETE"])
def delete_plant(_id):
    plant_to_delete = models.Plant.query.filter_by(id=_id).first()
    db.session.delete(plant_to_delete)
    db.session.commit()
    LOGGER.info(f"Deleted record: {plant_to_delete}")
    response_body = {"message": f"Plant (id: {_id}, name: {plant_to_delete.scientific_name}) deleted."}
    return flask.jsonify(response_body), 200


@app.route("/plant-family", methods=["POST"])
def add_plant_family():
    payload = flask.request.json
    plant_family_schema = models.PlantFamilySchema()
    plant_family = plant_family_schema.load(payload)
    db.session.add(plant_family)
    db.session.commit()
    return plant_family_schema.dumps(plant_family), 201


@app.errorhandler(orm_exc.UnmappedInstanceError)
def handle_unmapped_instance(error):
    response_body = util.create_error_message("referenced resource could not be found", error)
    return response_body, 404


@app.errorhandler(exceptions.ValidationError)
def handle_validation_error(error):
    response_body = util.create_error_message("input could not be validated", error)
    return response_body, 400


@app.errorhandler(exc.IntegrityError)
def handle_integrity_error(error):
    response_body = util.create_error_message("constraint violation", error)
    return response_body, 400


# Need to configure Swagger after url definitions
swagger = swagger.Swagger(app=app, title="Swagger page")
swagger.configure()


if __name__ == '__main__':
    app.run()
