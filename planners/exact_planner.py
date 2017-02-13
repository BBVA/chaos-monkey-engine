import logging
import arrow
from chaosmonkey.planners.planner import Planner


class ExactPlanner(Planner):
    """
    Schedule a single job for a specific date
    """

    ref = "exact_planner:ExactPlanner"
    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                }
            }
        }
    }
    example = {
        "ref": "exact_planner:ExactPlanner",
        "args": {
            "date": "2016-06-21T15:30:00"
        }
    }

    def __init__(self, name):
        super(ExactPlanner, self).__init__(name)

        self.log = logging.getLogger(__name__)

    def plan(self, planner_config, attack_config):
        plan = self.add_plan(self.name)

        attack_date = arrow.get(planner_config["args"]["date"]).datetime.replace(tzinfo=None)
        self.log.info("Exact Planner in %s", attack_date)
        self._add_executor(attack_date, self.name, attack_config, plan.id)

    @staticmethod
    def to_dict():
        return Planner._to_dict(ExactPlanner.ref, ExactPlanner.schema, ExactPlanner.example)
