import json

from marshmallow_jsonschema import JSONSchema


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


def get_first_type_name(type_metadata):
    return type_metadata[0] if type(type_metadata).__name__ == "list" else type_metadata


def get_schema_meta(schema_class):
    json_schema = JSONSchema()
    schema = schema_class()
    meta = json_schema.dump(schema)
    schema_name = schema.__class__.__name__
    properties = meta["definitions"][schema_name]["properties"]
    request_structure = {d["title"]: get_first_type_name(d["type"]) for d in properties.values()}
    return request_structure
