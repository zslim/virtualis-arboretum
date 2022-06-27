import json

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


def read_api_spec(host, port):
    oas_path = "../open_api_specification.yaml"
    yaml = YAML(typ="safe")
    with open(oas_path) as yaml_file:
        oas_dict = yaml.load(yaml_file)
    oas_dict["servers"][0] = {"url": f"http://{host}:{port}"}
    return oas_dict

