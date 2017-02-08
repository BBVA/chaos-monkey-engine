"""
Base class for planners

Every planner must extend Planner class
"""
from chaosmonkey.engine.cme_manager import manager


class Planner:
    """
    Planner interface
    Planners are responsible for scheduling jobs that executes attacks

    :param name:    plan name
    """

    ref = None  # must override
    schema = None  # must override
    example = None  # must override

    def __init__(self, name):
        self.name = name

    def plan(self, planner_config, attack_config):
        """
        Plan the jobs.
        This method should use the config to schedule jobs based on the
        configuration for the planner

        :param planner_config:    configuration related to the scheduler
        :param attack_config:   configuration related to the attack
        """
        raise NotImplementedError("Plans should implement this!")

    @staticmethod
    def add_plan(name):
        return manager.add_plan(name)

    @staticmethod
    def _add_executor(date, name, attack_config, plan_id):
        """
        Add a job to the global scheduler

        :param date: date to execute the job
        :param name: job name
        :param attack_config: configuration related to the attack
        """
        date_timezone = manager.scheduler.timezone.localize(date)
        manager.add_executor(date_timezone, name, attack_config, plan_id)

    @staticmethod
    def to_dict():
        raise NotImplementedError("Planners should implement this!")

    @staticmethod
    def _to_dict(ref, schema, example):
        return {
            "ref": ref,
            "schema": schema,
            "example": example,
        }
