from datetime import datetime, timedelta
from behave import then, given
from chaosmonkey.dal.database import db


@then(u'{n_executors} executors are created in the database')
def step_impl(context, n_executors):
    """make sure N executors exists in DB"""
    executors = context.manager.sql_store.get_executors()
    assert len(executors) == int(n_executors)
    context.executors = executors


@then(u'{n_plans} plans are created in the database')
def step_impl(context, n_plans):
    """make sure N plans exists in DB"""
    plans = context.manager.sql_store.get_plans()
    assert len(plans) == int(n_plans)
    context.plans = plans


@then(u'the executors are related to the created plan in the database')
def step_impl(context):
    """make N attacks available on the attack store"""
    plan = context.plans[0]
    for executor in context.executors:
        assert executor.plan_id == plan.id


@given(u'a plan exists in the database')
def step_impl(context):
    """Add a plan to the database"""
    plan = context.manager.add_plan("plan name")
    context.last_plan = plan


@given(u'{n_executors} executors for attack1 exists in the database related to the plan')
def step_impl(context, n_executors):
    """Add N executors related to the last_plan.id"""
    run_date = datetime.now() + timedelta(hours=10)
    context.executors_to_run = []
    for i in range(0, int(n_executors)):
        executor_conf = {"ref": "test.attacks.attack1:Attack1", "args": {}}
        executor = context.manager.add_executor(run_date, "exec name %s" % i, executor_conf, context.last_plan.id)
        context.executors_to_run.append(executor)


@then(u'no plans exists in the database')
def step_impl(context):
    """Add N executors related to the last_plan.id"""
    plans = context.manager.get_plans(show_all=True)
    assert len(plans) == 0


@then(u'no executors exists in the database')
def step_impl(context):
    """Add N executors related to the last_plan.id"""
    executors = context.manager.get_executors(executed=True)
    assert len(executors) == 0


@given(u'a plan marked as executed exists in the database')
def step_impl(context):
    """Add a plan to the database"""
    plan = context.manager.add_plan("plan name executed")
    plan.executed = True
    db.session.commit()


@then(u'the executor is marked as executed in the database')
def step_impl(context):
    """Check that context.last_executor_id is executed"""
    executor = context.manager.get_executor(context.last_executor_id)
    assert executor.executed is True


@then(u'the plan is marked as executed in the database')
def step_impl(context):
    """Check that context.last_plan.id is executed"""
    plan = context.manager.get_plan(context.last_plan.id)
    assert plan.executed is True
