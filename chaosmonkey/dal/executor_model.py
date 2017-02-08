from flask import request
from flask_hal.document import BaseDocument, link
from chaosmonkey.dal.database import db


class Executor(db.Model):
    """
    Executors are persistent representations of scheduled jobs.
    This model is shared between the cme and apscheduler.
    """

    __tablename__ = 'cme_executors'

    id = db.Column(db.String(80), primary_key=True)  #: unique identifier
    next_run_time = db.Column(db.DateTime, index=True)  #: DateTime for the executor to be executed
    job_state = db.Column(db.LargeBinary, nullable=False)  #: store the full state of the executor (with pickle)
    plan_id = db.Column(db.Integer, db.ForeignKey('cme_plans.id'))  #: plan id reference
    executed = db.Column(db.Boolean)  #: if the job was executed

    def __init__(self, job_id, next_run_time, plan_id, job_state=None):
        self.id = job_id
        self.next_run_time = next_run_time
        self.job_state = job_state
        self.plan_id = plan_id
        self.executed = False

    def to_dict(self):
        """
        Return a :meth:`flask_hal.document` representation for the Executor

        :return: :meth:`chaosmonkey.dal.executor_model.HalExecutor`
        """

        return HalExecutor(data={
            "id": self.id,
            "next_run_time": self.next_run_time.strftime('%Y-%m-%dT%H:%M:%s'),
            "plan_id": self.plan_id,
            "executed": self.executed
        }).to_dict()

    def __repr__(self):
        return '<Executor %r>' % self.id


class HalExecutor(BaseDocument):
    """
    Class to represent an Executor as a :meth:`flask_hal.document`
    """
    def __init__(self, data=None, links=None, embedded=None):
        super(HalExecutor, self).__init__(data, links, embedded)

        self.links.append(link.Link("self", request.path + data["id"]))
        self.links.append(link.Link("update", request.path + data["id"]))
        self.links.append(link.Link("delete", request.path + data["id"]))
