import logging
import random
from chaosmonkey.attacks.attack import Attack
from chaosmonkey.drivers import EC2DriverFactory


class TerminateEC2InstanceNotExcluded(Attack):
    """
    This attack module targets AWS instances.

    See {chaosmonkey.attacks.EC2DriverFactory} for info about how to provide
    credentials to access AWS.

    Terminate an EC2 instance, randomly selected by the filters provided but exclude those
    that match the excluded filter

    See https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html for
    available filters.
    """
    ref = "terminate_ec2_instance_not_excluded:TerminateEC2InstanceNotExcluded"

    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "region": {"type": "string"},
                    "filters": {
                        "type": "object",
                        "properties": {
                            "tag:Name": {"type": "string"}
                        }
                    },
                    "excluded": {
                        "type": "object",
                        "properties": {
                            "tag:Name": {"type": "string"}
                        }
                    }
                },
                "required": ["region", "filters", "excluded"]
            }
        }
    }
    
    example = {
        "ref": ref,
        "args": {
            "filters": {
                "tag:Team": "ateam"
            },
            "excluded": {
                "tag:Domain": "mongo"
            },
            "region": "eu-west-1"
        }
    }

    def __init__(self, attack_config):
        super(TerminateEC2InstanceNotExcluded, self).__init__(attack_config)

        self.log = logging.getLogger(__name__)

        region = self.attack_config.get("region", None)
        self.driver = EC2DriverFactory(region=region).get_driver()

    def run(self):
        nodes = self._get_nodes(self.attack_config.get("filters"), self.attack_config.get("excluded"))

        if len(nodes) <1:
            self.log.info("Unable to locate nodes to attack!! Tag excluded: %s ", self.attack_config.get("excluded"))
            return

        random.seed()
        node = random.choice(nodes)
        self.log.info("Destroy node (%s)", node.private_ips[0])

        self.driver.destroy_node(node)

    def _get_nodes(self, filters, excluded):
        """
        Return the nodes matching the filters, excluding some by tag
        """
        selected_nodes = []
        if "instance-state-name" not in filters:
            filters["instance-state-name"] = "running"

        self.log.info("Get nodes with filter: %r ", filters)

        nodes = self.driver.list_nodes(ex_filters=filters)
 
        for node in nodes:
            tags = self.driver.ex_describe_tags(node)

            if not (excluded.items() <= tags.items()):
                selected_nodes.append(node)

        return selected_nodes

    @staticmethod
    def to_dict():
        return Attack._to_dict(
            TerminateEC2InstanceNotExcluded.ref,
            TerminateEC2InstanceNotExcluded.schema,
            TerminateEC2InstanceNotExcluded.example
        )

