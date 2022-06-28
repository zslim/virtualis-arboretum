import os

import flask
from ruamel.yaml import YAML

blueprint = flask.Blueprint("swagger", __name__)


def read_api_spec():
    oas_file = "open_api_specification.yaml"
    oas_path = os.path.join(os.getcwd(), oas_file)
    yaml = YAML(typ="safe")
    with open(oas_path) as yaml_file:
        specification = yaml.load(yaml_file)
    return specification


@blueprint.get("/swagger/swagger.json")
def get_swagger_specification():
    swagger_json = read_api_spec()
    return flask.jsonify(swagger_json), 200


@blueprint.get("/")
@blueprint.get("/swagger")
def render_swagger_ui():
    return flask.render_template("swagger-index.html")
