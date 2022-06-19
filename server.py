import json
import logging

import flask
from marshmallow import exceptions
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc

import models
import util
from app_init import app, db

LOGGER = logging.getLogger(__name__)

# TODO: modularize routes and error handlers
# TODO: decide how the entry point is going to be


@app.route("/plants", methods=["GET"])
def get_plants():
    plants = models.Plant.query.all()
    plant_schema = models.PlantSchema(many=True)
    plants_json = plant_schema.dumps(plants)
    return plants_json


@app.route("/plant", methods=["POST"])
def add_plant():
    payload = flask.request.json
    plant_schema = models.PlantSchema()
    plant = plant_schema.load(payload)
    db.session.add(plant)
    db.session.commit()
    LOGGER.info(f"Created record: {plant}")
    response = flask.Response(plant_schema.dumps(plant), status=201)
    return response


@app.route("/plant/<_id>", methods=["DELETE"])
def delete_plant(_id):
    plant_to_delete = models.Plant.query.filter_by(id=_id).first()
    db.session.delete(plant_to_delete)
    db.session.commit()
    LOGGER.info(f"Deleted record: {plant_to_delete}")
    response_body = {"message": f"Plant (id: {_id}, name: {plant_to_delete.scientific_name}) deleted."}
    response = flask.Response(json.dumps(response_body), status=200, content_type="application/json")
    return response


@app.route("/plant-family", methods=["POST"])
def add_plant_family():
    payload = flask.request.json
    plant_family_schema = models.PlantFamilySchema()
    plant_family = plant_family_schema.load(payload)
    db.session.add(plant_family)
    db.session.commit()
    response = flask.Response(plant_family_schema.dumps(plant_family), status=201)
    return response


@app.errorhandler(orm_exc.UnmappedInstanceError)
def handle_unmapped_instance(error):
    response_body = util.create_error_message("referenced resource could not be found", error)
    response = flask.Response(response_body, status=404)
    return response


@app.errorhandler(exceptions.ValidationError)
def handle_validation_error(error):
    response_body = util.create_error_message("input could not be validated", error)
    response = flask.Response(response_body, status=400)
    return response


@app.errorhandler(exc.IntegrityError)
def handle_integrity_error(error):
    response_body = util.create_error_message("constraint violation", error)
    response = flask.Response(response_body, status=400)
    return response


if __name__ == '__main__':
    app.run()
