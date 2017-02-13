from chaosmonkey.attacks.attack import Attack


class RequiredSchema(Attack):

    ref = "required_schema:RequiredSchema"

    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "property1": {"type": "string"},
                    "property2": {"type": "string"},
                },
                "required": ["property1", "property2"]
            }
        }
    }

    example = {
        "ref": ref,
        "args": {
            "property1": "test1",
            "property2": "test2"
        }
    }

    def __init__(self, attack_config):
        super(RequiredSchema, self).__init__(attack_config)

    def run(self):
        pass

    @staticmethod
    def to_dict():
        return Attack._to_dict(
            RequiredSchema.ref,
            RequiredSchema.schema,
            RequiredSchema.example
        )
