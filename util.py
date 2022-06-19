import json


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
