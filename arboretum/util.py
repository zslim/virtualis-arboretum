import json
import os

from ruamel.yaml import YAML


def create_error_message(cause, error):
    payload = {
        "error": {
            "cause": cause,
            "exception": str(error.__class__),
            "description": str(error)
        }
    }
    payload_string = json.dumps(payload)
    return payload_string


def read_api_spec():
    oas_file = "open_api_specification.yaml"
    oas_path = os.path.join(os.getcwd(), oas_file)
    yaml = YAML(typ="safe")
    with open(oas_path) as yaml_file:
        oas_dict = yaml.load(yaml_file)
    return oas_dict

