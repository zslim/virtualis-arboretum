import json

import flask
from marshmallow import exceptions
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc

blueprint = flask.Blueprint("error_handlers", __name__)


def create_error_response(error, message, status_code):
    payload = {
        "error": {
            "cause": message,
            "exception": str(error.__class__),
            "description": str(error)
        }
    }
    response_body = json.dumps(payload)
    response = flask.Response(response_body, status_code, {"Content-Type": "application/json, charset=utf-8"})
    return response


@blueprint.app_errorhandler(orm_exc.UnmappedInstanceError)
def handle_unmapped_instance(error):
    error_message = "referenced resource could not be found"
    status_code = 404
    return create_error_response(error, error_message, status_code)


@blueprint.app_errorhandler(exceptions.ValidationError)
def handle_validation_error(error):
    error_message = "received data could not be validated"
    status_code = 400
    return create_error_response(error, error_message, status_code)


@blueprint.app_errorhandler(exc.IntegrityError)
def handle_integrity_error(error):
    error_message = "constraint violation"
    status_code = 400
    return create_error_response(error, error_message, status_code)


@blueprint.app_errorhandler(exc.DataError)
def handle_data_error(error):
    error_message = "invalid input"
    status_code = 400
    return create_error_response(error, error_message, status_code)


@blueprint.app_errorhandler(exc.OperationalError)
def handle_operational_error(error):
    error_message = "database connection could not be established"
    status_code = 500
    return create_error_response(error, error_message, status_code)


@blueprint.app_errorhandler(exc.PendingRollbackError)
def handle_pending_rollback_error(error):
    error_message = "session rollback pending"
    status_code = 500
    return create_error_response(error, error_message, status_code)
