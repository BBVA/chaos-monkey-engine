"""
**Base path**: /api/1/attacks

Attacks are python modules (located in /attacks folder) that are executed to perform actual attacks.

Each attack has three main properties represented in the API:

1. **example**: a JSON example for the attack. Use it as a template to call /plans endpoints
2. **ref**: its unique identifier. module_name:AttackClass
3. **schema**: json schema that validates the json representation for the attack

"""
from flask import Blueprint
from flask_hal import Document
from chaosmonkey.engine.cme_manager import manager

attacks = Blueprint("attacks", __name__)


@attacks.route("/", methods=["GET"])
def list_attacks():
    """
    Return a list with the available attacks and its configuration.

    Example::

        {
            "attacks": [
                {
                    "example": {
                        "args": {
                            "filters": {
                                "tag:Name": "playground-asg"
                            },
                            "region": "eu-west-1"
                        },
                        "ref": "terminate_ec2_instance:TerminateEC2Instance"
                    },
                    "ref": "terminate_ec2_instance:TerminateEC2Instance",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "args": {
                                "type": "object",
                                "properties": {
                                    "filters": {
                                        "type": "object",
                                        "properties": {
                                            "tag:Name": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "tag:Name"
                                        ]
                                    },
                                    "region": {
                                        "optional": true,
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "region",
                                    "filters"
                                ]
                            },
                            "ref": {
                                "type": "string"
                            }
                        }
                    }
                }
            ],
            "_links": {
                "self": {
                    "href": "/api/1/attacks/"
                }
            }
        }

    :return: :meth:`flask_hal.document`
    """
    attack_list = manager.get_attack_list()
    return Document(data={"attacks": attack_list})
