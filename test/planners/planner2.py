from chaosmonkey.planners.planner import Planner


class Planner2(Planner):
    """
    Schedule a single job for a specific date
    """

    ref = "planner1:Planner2"
    schema = {}
    example = {}

    def plan(self, planner_config, attack_config):
        pass

    @staticmethod
    def to_dict():
        return Planner._to_dict(Planner2.ref, Planner2.schema, Planner2.example)
