from chaosmonkey.planners.planner import Planner


class Planner1(Planner):
    """
    Schedule a single job for a specific date
    """

    ref = "planner1:Planner1"
    schema = {}
    example = {}

    def plan(self, planner_config, attack_config):
        pass

    @staticmethod
    def to_dict():
        return Planner._to_dict(Planner1.ref, Planner1.schema, Planner1.example)
