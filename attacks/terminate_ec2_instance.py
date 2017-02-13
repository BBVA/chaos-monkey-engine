import logging
import random
from chaosmonkey.attacks.attack import Attack
from chaosmonkey.drivers.ec2_driver import EC2DriverFactory


class TerminateEC2Instance(Attack):
    """
    This attack module targets AWS instances.

    See {chaosmonkey.attacks.ec2_provider.EC2DriverFactory} for info about how to provide
    credentials to access AWS.

    Terminate an EC2 instance, randomly selected by the filters provided
    See https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html for
    available filters.
    """
    ref = "terminate_ec2_instance:TerminateEC2Instance"

    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "optional": True},
                    "filters": {
                        "type": "object",
                        "properties": {
                            "tag:Name": {"type": "string"}
                        }
                    }
                },
                "required": ["filters", "region"]
            }
        }
    }

    example = {
        "ref": ref,
        "args": {
            "filters": {
                "tag:Name": "playground-asg"
            },
            "region": "eu-west-1"
        }
    }

    def __init__(self, attack_config):
        super(TerminateEC2Instance, self).__init__(attack_config)

        self.log = logging.getLogger(__name__)

        region = self.attack_config.get("region", None)
        self.driver = EC2DriverFactory(region=region).get_driver()

    def run(self):
        nodes = self._get_nodes(self.attack_config.get("filters"))
        random.seed()
        node = random.choice(nodes)
        self.log.info("Destroy node (%s)", node.private_ips[0])

        self.driver.destroy_node(node)

    def _get_nodes(self, filters):
        """
        Return the nodes matching the filters
        """
        if "instance-state-name" not in filters:
            filters["instance-state-name"] = "running"

        self.log.info("Get nodes with filter: %r ", filters)

        nodes = self.driver.list_nodes(ex_filters=filters)
        return nodes

    @staticmethod
    def to_dict():
        return Attack._to_dict(
            TerminateEC2Instance.ref,
            TerminateEC2Instance.schema,
            TerminateEC2Instance.example
        )
