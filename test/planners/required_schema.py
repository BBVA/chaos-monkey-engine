from chaosmonkey.planners.planner import Planner


class RequiredSchema(Planner):

    schema = {
        "type": "object",
        "properties": {
            "property1": {"type": "string"},
            "property2": {"type": "string"},
        },
        "required": ["property1", "property2"]
    }

    example = {
        "property1": "test1",
        "property2": "test2"
    }

    ref = "required_schema:RequiredSchema"

    def plan(self, planner_config, attack_config):
        pass

    @staticmethod
    def to_dict():
        return Planner._to_dict(RequiredSchema.ref, RequiredSchema.schema, RequiredSchema.example)
