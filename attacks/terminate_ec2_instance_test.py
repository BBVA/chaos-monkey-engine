import pytest
from unittest.mock import patch
from jsonschema import validate, ValidationError
from copy import deepcopy

attack_module = __import__("terminate_ec2_instance")

valid_attack_config = {
    "args": {
        "filters": {
            "tag:Name": "playground-asg"
        },
        "region": "eu-west-1"
    }
}


class NodeMock:
    def __init__(self):
        self.private_ips = ["localhost"]


def test_attack_validates_missing_filters():
    invalid_conf = deepcopy(valid_attack_config)
    invalid_conf.get("args").pop("filters")
    attack = attack_module.TerminateEC2Instance(invalid_conf.get("args"))
    with pytest.raises(ValidationError):
        validate(invalid_conf, attack.schema)


def test_valid_attack_config():
    with patch.object(attack_module, "EC2DriverFactory") as EC2DriverFactory_mock:
        attack = attack_module.TerminateEC2Instance(valid_attack_config.get("args"))
        assert attack.driver is not None
        EC2DriverFactory_mock.assert_called_once_with(region=valid_attack_config.get("args").get("region"))
        EC2DriverFactory_mock.return_value.get_driver.assert_called_once_with()


def test_run_should_destroy_node():
    with patch.object(attack_module.TerminateEC2Instance, "_get_nodes") as get_nodes_mock, \
            patch.object(attack_module, "EC2DriverFactory") as EC2DriverFactory_mock:

        node_mocked = NodeMock()
        get_nodes_mock.return_value = [node_mocked]

        attack = attack_module.TerminateEC2Instance(valid_attack_config.get("args"))
        attack.run()
        EC2DriverFactory_mock.return_value.get_driver.return_value.destroy_node.assert_called_once_with(node_mocked)


def test_get_nodes_should_add_addition_filter():
    with patch.object(attack_module, "EC2DriverFactory") as EC2DriverFactory_mock:

        attack = attack_module.TerminateEC2Instance(valid_attack_config.get("args"))
        filters = valid_attack_config.get("args").get("filters")
        attack._get_nodes(filters.copy())

        filters["instance-state-name"] = "running"

        EC2DriverFactory_mock.return_value.get_driver.return_value\
            .list_nodes.assert_called_once_with(ex_filters=filters)


def test_attack_example_validates():
    attack = attack_module.TerminateEC2Instance(valid_attack_config.get("args"))
    try:
        validate(valid_attack_config, attack.schema)
    except ValidationError:
        assert True is False
