from chaosmonkey.api.api_errors import APIError
from jsonschema import validate, ValidationError


def validate_payload(request, schema):
    """
    validates a request payload against a json schema

    :param request: request received with valid json body
    :param schema:  schema to validate the request payload

    :return: True
    :raises: :meth:`chaosmonkey.api.api_errors`
    """
    try:
        json = request.get_json()
        validate(json, schema)
    except ValidationError as e:
        raise APIError("invalid payload %s" % e.message)
    except Exception:
        raise APIError("payload must be a valid json")
    else:
        return True
