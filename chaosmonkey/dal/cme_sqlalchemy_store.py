"""
CMESQLAlchemyStore replaces the default SQLAlchemyJobstore from
`apscheduler <http://apscheduler.readthedocs.io/>`_

It controls the persistence layer.
"""
import logging

from apscheduler.job import Job
from apscheduler.jobstores.base import BaseJobStore, JobLookupError
from sqlalchemy import text
from chaosmonkey.engine.cme_manager import manager
from chaosmonkey.dal.executor_model import Executor
from chaosmonkey.dal.plan_model import Plan
from chaosmonkey.dal.database import db

try:
    import cPickle as pickle
except ImportError:  # pragma: nocover
    import pickle


class CMESQLAlchemyStore(BaseJobStore):
    """
    CMESQLAlchemyStore

    Manage persistence for `apscheduler <http://apscheduler.readthedocs.io/>`_
    and CMEEngine.

    This class is used by the apscheduler, all overridden methods should
    return appscheduler.job.Job objects.

    The store handles 2 types of models: plans and executors.
    Internally apscheduler names the executors as jobs.

    TODO: executors are marked as executed when they are processed
        (no mather if they fail or succeed. We need to handle execution errors
        in order to know whats going on with the execution and what was its result.)

    * Plans: :meth:`chaosmonkey.dal.plan_model.Plan`
    * Executors: :meth:`chaosmonkey.dal.executor_model.Executor`
    """

    def __init__(self, pickle_protocol=pickle.HIGHEST_PROTOCOL):
        super(CMESQLAlchemyStore, self).__init__()  # pylint: disable=no-member
        self.pickle_protocol = pickle_protocol
        self.log = logging.getLogger(__name__)

    def start(self, scheduler, alias):
        """
        Start the SQLAlchemy engine
        """
        super(CMESQLAlchemyStore, self).start(scheduler, alias)

    def lookup_job(self, job_id):
        job = Executor.query.get(job_id)
        if not job:
            raise JobLookupError("job with id %s not found" % job_id)
        else:
            return self._reconstitute_job(job.job_state) if job.job_state else None

    def get_due_jobs(self, now):
        return self._get_jobs(Executor.next_run_time <= now)

    def get_next_run_time(self):
        job = Executor.query.order_by(Executor.next_run_time).limit(1).all()
        next_run_time = None
        if len(job) > 0:
            next_run_time = manager.scheduler.timezone.localize(job[0].next_run_time)
        return next_run_time

    def get_all_jobs(self):
        jobs = self._get_jobs()
        self._fix_paused_jobs_sorting(jobs)
        return jobs

    def add_job(self, job):
        job_state = pickle.dumps(job.__getstate__(), self.pickle_protocol)
        job = Executor(job.id, job.next_run_time, job.kwargs.get("plan_id"), job_state)
        db.session.add(job)
        db.session.commit()
        self._check_plan_executed(job.id)

    def update_job(self, job):
        job_model = Executor.query.get(job.id)
        job_model.next_run_time = job.next_run_time
        job_model.job_state = pickle.dumps(job.__getstate__(), self.pickle_protocol)
        db.session.commit()

    def remove_job(self, job_id):
        """
        Instead of deleting a job when its executed or it has failed, check it as executed.

        TODO: delete the executor and save to a historic table the executed attacks with its
        logs and results.
        """
        job_model = Executor.query.get(job_id)
        if job_model is None:
            raise JobLookupError(job_id)

        job_model.executed = True
        db.session.commit()

        self._check_plan_executed(job_id)

    def real_remove_job(self, job_id):
        self.log.debug('real remove job %s', job_id)
        job_model = Executor.query.get(job_id)
        if job_model is None:
            raise JobLookupError(job_id)

        db.session.delete(job_model)
        db.session.commit()

    def remove_all_jobs(self):
        db.session.query(Executor).delete()
        db.session.commit()

    def shutdown(self):
        pass

    def _reconstitute_job(self, job_state):
        job_state = pickle.loads(job_state)
        job_state['jobstore'] = self
        job = Job.__new__(Job)
        job.__setstate__(job_state)
        job._scheduler = self._scheduler  # pylint: disable=protected-access
        job._jobstore_alias = self._alias  # pylint: disable=protected-access
        return job

    def _get_jobs(self, *conditions):
        """
        Return only jobs with executed == 0. Because we are not deleting the executors we need
          to filter to ensure the apscheduler gets only pending jobs
        """
        job_list = []
        jobs = db.session.query(Executor).filter(Executor.executed == 0, *conditions)

        failed_job_ids = set()
        for job in jobs:
            try:
                job_list.append(self._reconstitute_job(job.job_state))
            except:  # pylint: disable=bare-except
                self.log.exception('Unable to restore job "%s" -- removing it', job.id)
                failed_job_ids.add(job.id)

        # Remove all the jobs we failed to restore
        if failed_job_ids:
            Executor.query.filter(Executor.id.in_(failed_job_ids))

        return job_list

    # Custom methods.
    # Methods defined bellow are only used by the CMEManager and must only return
    # db.Models (chaosmonkey.dal.*_model)

    def _check_plan_executed(self, executor_id):
        """
        Each time a executor is marked as executed check if all executors in the plan
        are executed and check the plan as executed as well

        :param executor_id: string
        :return:
        """
        executor = Executor.query.get(executor_id)
        if executor:
            plan = Plan.query.get(executor.plan_id)

            self.log.debug('check if all executors in plan %s are executed', executor.plan_id)
            # get all executor for the same plan that are not executed
            # pylint: disable=singleton-comparison
            executors_pending = Executor.query.\
                filter(Executor.executed == False, Executor.plan_id == executor.plan_id).all()
            if len(executors_pending) == 0:
                self.log.debug('all executors has been executed for the plan %s', executor.plan_id)
                # if no executors are pending to execute, mark the pan as executed

                plan.executed = True
            else:
                self.log.debug('there are executors pending in plan %s', executor.plan_id)
                plan.executed = False

            db.session.commit()

    def get_executor(self, executor_id):
        """
        Get an executor

        :param executor_id: string
        :return: List of Executor
        """
        self.log.debug('get executor %s', executor_id)
        return Executor.query.get(executor_id)

    def get_executors(self, executed=False):
        """
        Get a list of executors

        :return: List of Executor
        """
        self.log.debug('get all executors in store with executed %s', executed)
        return Executor.query.filter(Executor.executed == executed)\
            .order_by(Executor.next_run_time).all()

    def get_executors_for_plan(self, plan_id):
        """
        Get a list of executors related to a plan by its plan_id

        :param plan_id: string
        :return: List of Executor
        """
        self.log.debug('get executors for plan %s', plan_id)
        return db.session.query(Executor).filter(Executor.plan_id == plan_id)

    def add_plan(self, name):
        """
        Create a plan in the db.

        :param name: string
        :return: Plan created
        """
        self.log.debug('create plan %s', name)
        plan = Plan(name=name)
        db.session.add(plan)
        db.session.commit()
        return plan

    def get_plans(self, show_all=False):
        """
        Return a list of plans created on db. For each plan return the number of pending executors and the
        next_run_time of the first executor

        :return: List of Plans
        """

        query = 'SELECT ' \
                'cme_plans.id, name, created, COUNT(cme_executors.id) as executors_count, ' \
                ' MIN(next_run_time), cme_plans.executed ' \
                'FROM cme_plans ' \
                'LEFT JOIN cme_executors ON cme_plans.id == cme_executors.plan_id ' \

        if show_all is False:
            query += 'WHERE cme_plans.executed == 0 '

        query += 'GROUP BY cme_plans.id'
        self.log.debug('get plans query %s', query)
        sql = text(query)
        result = db.engine.execute(sql)
        plans = []
        for row in result:
            plan = Plan(
                _id=row[0],
                name=row[1],
                created=row[2],
                executors_count=row[3],
                next_execution=row[4],
                executed=row[5]
            )
            plans.append(plan)

        return plans

    def get_plan(self, plan_id):
        """
        Return a plan by its id

        :param plan_id: string
        :return: Plan
        """
        self.log.debug('get plan %s', plan_id)
        plan = Plan.query.get(plan_id)
        return plan

    def delete_plan(self, plan_id):
        """
        Delete a plan.

        All the executors related to the plan are deleted. (ON_DELETE constrain in db.Models)

        :param plan_id: string
        """
        self.log.debug('delete plan %s', plan_id)
        plan = Plan.query.get(plan_id)
        if plan:
            db.session.delete(plan)
            db.session.commit()
        else:
            raise PlanLookupError(plan_id)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class PlanLookupError(KeyError):
    """Raised when the store cannot find a plan for update or removal."""

    def __init__(self, job_id):
        super(PlanLookupError, self).__init__(u'No plan by the id of %s was found' % job_id)
