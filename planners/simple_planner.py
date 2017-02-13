import logging
import random
from datetime import datetime
from chaosmonkey.planners.planner import Planner


class SimplePlanner(Planner):
    """
    Schedule an attack for today, N times between two given times

    Planner config must contain the following args:
    """

    ref = "simple_planner:SimplePlanner"
    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "min_time": {"type": "string"},
                    "max_time": {"type": "string"},
                    "times": {"type": "number"},
                }
            }
        }
    }
    example = {
        "ref": "simple_planner:SimplePlanner",
        "args": {
            "min_time": "10:00",
            "max_time": "15:00",
            "times": 4
        }
    }

    def __init__(self, name):
        super(SimplePlanner, self).__init__(name)

        self.log = logging.getLogger(__name__)
        self.planner_config = None

    def plan(self, planner_config, attack_config):
        self.planner_config = planner_config

        plan = self.add_plan(self.name)

        attack_dates = self._get_day_attack_schedule()
        self.log.debug("Day Planner in %s", attack_dates)
        for i, date in enumerate(attack_dates):
            self._add_executor(date, "-".join((self.name, str(i + 1))), attack_config, plan.id)
            self.log.info("Job scheduled for %s", date)

    def _get_day_attack_schedule(self):
        """
        Return an array of datetimes according to the planner args
        """
        planer_args = self.planner_config["args"]
        start_time = datetime.strptime(planer_args["min_time"], "%H:%M").time()
        start_date = datetime.combine(datetime.today().date(), start_time)
        end_time = datetime.strptime(planer_args["max_time"], "%H:%M").time()
        end_date = datetime.combine(datetime.today().date(), end_time)

        random.seed()
        attack_schedule = []
        for start, end in self._split_date_range(start_date, end_date, planer_args["times"]):
            attack_schedule.append(random.uniform(start, end))

        return attack_schedule

    @staticmethod
    def _split_date_range(start, end, intv):
        """
        Splits a daterange in even buckets
        """
        previous = start
        diff = (end - start) / intv
        for i in range(1, intv):
            current = start + diff * i
            yield (previous, current)
            previous = current
        yield (previous, end)

    @staticmethod
    def to_dict():
        return Planner._to_dict(SimplePlanner.ref, SimplePlanner.schema, SimplePlanner.example)
