from datetime import datetime, timedelta
from behave import when, then, given
from apscheduler.triggers.date import DateTrigger
from time import sleep
from chaosmonkey.dal.database import db


@when(u'the scheduler executes it')
def step_impl(context):
    """run the executor in context.executors_to_run"""
    for executor in context.executors_to_run:
        now = datetime.now() + timedelta(seconds=2)
        trigger = DateTrigger(run_date=now)
        context.manager.update_executor_trigger(executor.id, trigger)

        # give time to execute the jobs
        wait_for_job_executed(context, executor.id)

        context.last_executor_id = executor.id


def wait_for_job_executed(context, job_id):

    while True:
        executor = context.manager.get_executor(job_id)

        print(executor)
        print(executor.executed)
        if executor.executed:
            break
        else:
            db.session.expire(executor)

        sleep(0.5)

