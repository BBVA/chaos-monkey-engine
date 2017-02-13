from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship
from flask import request
from flask_hal.document import BaseDocument, link
from chaosmonkey.dal.database import db
from chaosmonkey.dal.executor_model import Executor


class Plan(db.Model):
    """
    Store information about the plan and its executors.

    This model is only used by the cme.
    """
    __tablename__ = 'cme_plans'

    id = db.Column(db.String(80), primary_key=True)  #: unique identifier
    name = db.Column(db.String(200), unique=False)  #: plan name
    created = db.Column(db.DateTime, unique=True)  #: creation datetime
    executed = db.Column(db.Boolean)  #: if all the executors in the plan has been executed

    next_execution = None  #: DateTime for the next executor execution time
    executors_count = None  #: number of pending executors

    jobs = relationship(Executor, cascade='all, delete, delete-orphan')

    # pylint: disable=too-many-arguments
    def __init__(self, _id=None, name=None, created=None, next_execution=None, executors_count=0, executed=False):
        self.id = _id or uuid4().hex
        self.name = name
        if created:
            self.created = datetime.strptime(created, '%Y-%m-%d %H:%M:%S.%f')
        else:
            self.created = datetime.utcnow()
        self.executed = executed
        self.next_execution = next_execution
        self.executors_count = executors_count

    def to_dict(self):
        """
        Returns a :meth:`flask_hal.document` representation for the Executor

        :return: :meth:`chaosmonkey.dal.plan_model.HalPlan`
        """

        return HalPlan(data={
            'id': self.id,
            'name': self.name,
            'created': self.created.strftime('%Y-%m-%dT%H:%M:%s'),
            'executors_count': self.executors_count,
            'next_execution': self.next_execution,
            'executed': self.executed
        }).to_dict()

    def __repr__(self):
        return '<Plan %r>' % self.name


class HalPlan(BaseDocument):
    """
    Class to represent a Plan as a :meth:`flask_hal.document`
    """
    def __init__(self, data=None, links=None, embedded=None):
        super(HalPlan, self).__init__(data, links, embedded)

        self.links.append(link.Link("self", request.path + data["id"]))
        self.links.append(link.Link("update", request.path + data["id"]))
        self.links.append(link.Link("delete", request.path + data["id"]))
