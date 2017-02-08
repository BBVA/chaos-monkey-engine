import pytest
from jsonschema import validate, ValidationError
from unittest.mock import patch
from copy import deepcopy

attack_module = __import__("api_request")

valid_attack_config = {
    "args": {
        "endpoint": "http://localhost:4500",
        "method": "GET",
        "payload": {"test": "1"},
        "headers": {"X-CUSTOM-HEADER": "test"}
    }
}


def test_run_should_make_a_request_with_config():
    with patch.object(attack_module.requests, "request") as request_mock:
        args = valid_attack_config.get("args")
        attack = attack_module.ApiRequest(args)
        attack.run()
        request_mock.assert_called_once_with(
            args.get("method"),
            args.get("endpoint"),
            headers=args.get("headers"),
            data=args.get("payload")
        )


def test_attack_validates_missing_endpoint():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("endpoint")
    attack = attack_module.ApiRequest(invalid_conf)
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_attack_validates_missing_method():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("method")
    attack = attack_module.ApiRequest(invalid_conf)
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_attack_validates_valid_config():
    attack = attack_module.ApiRequest(valid_attack_config)
    try:
        validate(valid_attack_config, attack.schema)
    except ValidationError as e:
        assert e is None
