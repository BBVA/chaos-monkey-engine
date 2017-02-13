from datetime import datetime, timedelta
from chaosmonkey.planners.planner import Planner


class TwoExecutors(Planner):
    """
    Schedule two executors
    """

    ref = "two_executors:TwoExecutors"
    schema = {}
    example = {}

    def plan(self, planner_config, attack_config):
        plan = self.add_plan(self.name)
        attack_date = datetime.now() + timedelta(hours=10)
        self._add_executor(attack_date, self.name, attack_config, plan.id)
        attack_date = attack_date + timedelta(hours=1)
        self._add_executor(attack_date, self.name, attack_config, plan.id)

    @staticmethod
    def to_dict():
        return Planner._to_dict(TwoExecutors.ref, TwoExecutors.schema, TwoExecutors.example)
