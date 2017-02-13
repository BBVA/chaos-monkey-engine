import logging
import requests
from chaosmonkey.attacks.attack import Attack


class ApiRequest(Attack):
    """
    This attack module makes calls to any API endpoint with any method, payload or header
    """

    ref = "api_request:ApiRequest"

    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string"},
                    "method": {"type": "string"},
                    "payload": {"type": "object"},
                    "headers": {"type": "object"}
                },
                "required": ["endpoint", "method", "payload", "headers"]
            }
        }
    }

    example = {
        "ref": ref,
        "args": {
            "endpoint": "http://localhost:4500",
            "method": "GET",
            "payload": {"test": "1"},
            "headers": {"X-CUSTOM-HEADER": "test"},
        }
    }

    def __init__(self, attack_config):
        super(ApiRequest, self).__init__(attack_config)
        self.log = logging.getLogger(__name__)

    def run(self):
        endpoint = self.attack_config.get("endpoint")
        method = self.attack_config.get("method")
        payload = self.attack_config.get("payload")
        headers = self.attack_config.get("headers")

        self.log.debug('running attack to (%s) %s', endpoint, method)

        requests.request(method, endpoint, headers=headers, data=payload)

    @staticmethod
    def to_dict():
        return Attack._to_dict(
            ApiRequest.ref,
            ApiRequest.schema,
            ApiRequest.example
        )
