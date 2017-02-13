"""
CME Manager

Control layer for CME Engine
"""
import logging

from jsonschema import validate, ValidationError
from chaosmonkey.dal.executor_model import Executor
from chaosmonkey.api.api_errors import APIError
from chaosmonkey.modules.module_store import ModuleLookupError


class CMEManager:
    """
    CMEManager is the manager responsible of communicating the API with the backend.

    It manages:

    * scheduler: BackgroundScheduler from appscheduler lib. The scheduler run executors
    * sql_store: SQLAlchemy store. The persistence layer
    * planners_store: ModuleStore that load and manages available planners.
    * attacks_store: ModuleStore that load and manage available attacks.

    Methods to interact with Executors and Plans always returns the db.Models (chaosmonkey.dal.*_model)

    Methods that interact with Attacks always returns Attacks objects (chaosmonkey.attacks.attack)

    Methods that interact with Planners always returns Planners objects (chaosmonkey.planners.planner)
    """
    def __init__(self):
        self._scheduler = None
        self._sql_store = None
        self._planners_store = None
        self._attacks_store = None
        self.log = logging.getLogger(__name__)

    def configure(self, scheduler, sql_store, planners_store, attacks_store):
        """
        Configure the manager

        :param scheduler:       apscheduler.schedulers.background.BackgroundScheduler
        :param sql_store:       SQLAlchemy
        :param planners_store:  chaosmonkey.modules.ModuleStore
        :param attacks_store:   chaosmonkey.modules.ModuleStore
        :return:
        """
        self._scheduler = scheduler
        self._sql_store = sql_store
        self._planners_store = planners_store
        self._attacks_store = attacks_store
        self.log.debug('CMEManager configured')

    @property
    def scheduler(self):
        """ Scheduler property """
        return self._scheduler

    @property
    def attacks_store(self):
        """ Attacks store property """
        return self._attacks_store

    @property
    def planners_store(self):
        """ Planners store property """
        return self._planners_store

    @property
    def sql_store(self):
        """ SQLstore property """
        return self._sql_store

    def get_executors(self, executed=False):
        """
        Return a list of Executor objects created in DB
        :return: chaosmonkey.dal.executor.Executor list
        """
        return self._sql_store.get_executors(executed=executed)

    def get_executor(self, executor_id):
        """
        Return an Executor object with the given id
        :return: chaosmonkey.dal.executor.Executor
        """
        return self._sql_store.get_executor(executor_id)

    def get_executors_for_plan(self, plan_id):
        """
        Return a list of Executors for a given plan id
        :return: chaosmonkey.dal.executor.Executor
        """
        return self.sql_store.get_executors_for_plan(plan_id)

    def update_executor_trigger(self, executor_id, trigger):
        """
        Update an executor trigger to change is due date

        :param executor_id: executor id
        :param trigger: apscheduler.triggers.BaseTrigger instance
        :return:        chaosmonkey.dal.executor.Executor
        """
        job = self._scheduler.reschedule_job(job_id=executor_id, trigger=trigger)
        return self._job_to_executor(job)

    def remove_executor(self, executor_id):
        """
        Removes an executor by his ID
        :param executor_id:
        :return:
        """
        self._scheduler.remove_job(job_id=executor_id)
        self.sql_store.real_remove_job(job_id=executor_id)

    def add_executor(self, date, name, attack_config, plan_id):
        """
        Adds a new executor to the scheduler

        :param date:            Datetime to execute the job
        :param name:            Executor name
        :param attack_config:   Attack config. Dict to be passed to the executor on execution time
        :param plan_id:         Referenced plan id
        :return:                chaosmonkey.dal.executor.Executor
        """
        from chaosmonkey.attacks.executor import execute
        self.log.debug('add scheduled job %s at %s', name, date)
        job = self._scheduler.add_job(
            execute,
            name=name,
            kwargs={
                "attack_config": attack_config,
                "plan_id": plan_id
            },
            trigger='date',
            run_date=date
        )

        return self._job_to_executor(job)

    def get_attack_list(self):
        """
        Return a list with all attacks loaded in the self._attacks_store

        :return: chaosmonkey.attacks.attack.Attack list
        """
        attacks_list = [self._attacks_store.get(attack_ref).to_dict() for attack_ref in self.attacks_store.list()]
        return attacks_list

    def get_planner_list(self):
        """
        Return a list with all planners loaded in the self._planners_store

        :return: chaosmonkey.planners.planner.Planner list
        """
        planner_list = [self._planners_store.get(planner_ref).to_dict() for planner_ref in self.planners_store.list()]
        return planner_list

    def execute_plan(self, name, planner_config, attack_config):
        """
        Execute a plan with a planner and executor config to create executors based on the configs

        It also validates the planner and executor config against the modules

        :param name:                Plan name
        :param planner_config:      Dict with planner config
        :param attack_config:       Dict with attack config
        """
        try:
            planner_class = self._planners_store.get(planner_config.get("ref"))
            attack_class = self._attacks_store.get(attack_config.get("ref"))
        except ModuleLookupError as e:
            raise APIError("invalid planner %s" % e.message)

        # Validate both executor and planner configs
        try:
            validate(planner_config.get("args"), planner_class.schema)
            validate(attack_config, attack_class.schema)
        except ValidationError as e:
            raise APIError("invalid payload %s" % e.message)

        planner = planner_class(name)
        planner.plan(planner_config, attack_config)

    def add_plan(self, name):
        """
        Creates a new plan in the sqlStore

        :param name:    Plan name
        :return:        chaosmonkey.dal.plan.Plan
        """
        return self._sql_store.add_plan(name)

    def get_plan(self, plan_id):
        """
        Returns a plans

        :return: chaosmonkey.dal.plan.Plan
        """
        return self._sql_store.get_plan(plan_id)

    def get_plans(self, show_all=None):
        """
        Returns a list with al plans in the sqlStore

        :return: List of chaosmonkey.dal.plan.Plan
        """
        return self._sql_store.get_plans(show_all=show_all)

    def delete_plan(self, plan_id):
        """
        Delete a plan (and all his associated executors) from the sqlStore

        :param plan_id:     String plan Id
        :return:
        """
        self._sql_store.delete_plan(plan_id)

    @staticmethod
    def _job_to_executor(job):
        """
        Converts a apscheduler.job.Job to chaosmonkey.dal.executor.Executor

        :param job:
        :return:
        """
        return Executor(
            job.id,
            job.next_run_time,
            job.kwargs.get("plan_id")
        )


manager = CMEManager()
