import pytest
from jsonschema import validate, ValidationError
from copy import deepcopy

attack_module = __import__("run_script")

valid_attack_config = {
    "args": {
        "region": "eu-west-1",
        "local_script": "/attacks/scripts/s_burncpu.sh",
        "remote_script": "/tmp/s_burncpu.sh",
        "filters": {
            "tag:Name": "playground-asg"
        },
        "ssh": {
            "user": "ec2-user",
            "pem": "BASE64_STRING_PEM"
        }
    }
}


def test_attack_validates_missing_ssh():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("ssh")
    attack = attack_module.RunScript(invalid_conf.get("args"))
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_attack_validates_missing_local_script():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("local_script")
    attack = attack_module.RunScript(invalid_conf.get("args"))
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_attack_validates_missing_remote_script():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("remote_script")
    attack = attack_module.RunScript(invalid_conf.get("args"))
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_attack_validates_missing_filters():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("filters")
    attack = attack_module.RunScript(invalid_conf.get("args"))
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_attack_validates_valid_config():
    attack = attack_module.RunScript(valid_attack_config.get("args"))
    try:
        validate(valid_attack_config.get("args"), attack.schema)
    except ValidationError as e:
        assert e is None
    else:
        pass
