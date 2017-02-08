"""
API Tests
"""
import arrow
from apscheduler.triggers.date import DateTrigger
from flask import url_for
from flask_hal import Document
from datetime import datetime, timedelta

from chaosmonkey.api.executors_blueprint import trigger_to_dict, dict_to_trigger


def test_executors_list_return_empty_array(app):
    url = url_for("executors.get_executors")

    with app.test_request_context(url):

        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(embedded={"executors": []}).to_dict()


def test_get_executors(app, manager, plan):
    """" Test that the endpoint returns an array of executors """
    url = url_for("executors.get_executors")

    run_time = datetime.now() + timedelta(hours=10)
    executor = manager.add_executor(run_time, "executor name", {}, plan.id)

    with app.test_request_context(url):
        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(embedded={"executors": [executor.to_dict()]}).to_dict()


def test_put_executor_valid_body(app, manager, plan):
    # Add a executor to the datastore
    run_time = datetime.now() + timedelta(hours=10)
    executor = manager.add_executor(run_time, "executor name", {}, plan.id)

    # Make the request
    url = url_for("executors.put_executor", executor_id=executor.id)
    with app.test_request_context(url):
        data = '{"type": "date", "args": {"date": "%s"}}' % run_time.strftime('%Y-%m-%dT%H:%M:%s%z')
        res = app.test_client().put(url,
                                    content_type="application/json",
                                    data=data)

    assert res.status_code == 200
    assert res.mimetype == "application/hal+json"


def test_put_executor_missing_trigger_type(app):
    url = url_for("executors.put_executor", executor_id="123")
    run_time = datetime.now() + timedelta(hours=10)

    with app.test_request_context(url):
        data = '{"args":{"date":"%s"}}' % run_time.strftime('%Y-%m-%dT%H:%M:%s%z')
        res = app.test_client().put(url_for("executors.put_executor", executor_id="123"),
                                    content_type="application/json",
                                    data=data)

    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json == {"msg": "invalid payload 'type' is a required property"}


def test_put_executor_invalid_trigger_type(app):
    url = url_for("executors.put_executor", executor_id="123")
    run_time = datetime.now() + timedelta(hours=10)

    with app.test_request_context(url):
        data = '{"type":"invalid", "args":{"date":"%s"}}' % run_time.strftime('%Y-%m-%dT%H:%M:%s%z')
        res = app.test_client().put(url_for("executors.put_executor", executor_id="123"),
                                    content_type="application/json",
                                    data=data)

    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json == {"msg": "Invalid trigger type"}


def test_put_executor_missing_trigger_args(app):
    url = url_for("executors.put_executor", executor_id="123")

    with app.test_request_context(url):
        data = '{"type":"date"}'
        res = app.test_client().put(url_for("executors.put_executor", executor_id="123"),
                                    content_type="application/json",
                                    data=data)

    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json == {"msg": "invalid payload 'args' is a required property"}


def test_put_executor_invalid_trigger_date(app):
    url = url_for("executors.put_executor", executor_id="123")

    with app.test_request_context(url):
        data = '{"type":"date","args":{"date":"invaliddate"}}'
        res = app.test_client().put(url_for("executors.put_executor", executor_id="123"),
                                    content_type="application/json",
                                    data=data)

    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json == {"msg": "Invalid date format"}


def test_put_executor_valid_body_invalid_executorid(app):
    url = url_for("executors.put_executor", executor_id="123")
    run_time = datetime.now() + timedelta(hours=10)

    with app.test_request_context(url):
        data = '{"type": "date", "args": {"date":"%s"}}' % run_time.strftime('%Y-%m-%dT%H:%M:%s%z')
        res = app.test_client().put(url_for("executors.put_executor", executor_id="invalid"),
                                    content_type="application/json",
                                    data=data)

    assert res.status_code == 404
    assert res.mimetype == "application/json"
    assert res.json == {"msg": "executor not found invalid"}


def test_delete_executor(app, manager, plan):
    # Add a executor to the datastore
    run_time = datetime.now() + timedelta(hours=10)
    executor = manager.add_executor(run_time, "executor name", {}, plan.id)
    url = url_for("executors.delete_executor", executor_id=executor.id)
    with app.test_request_context(url):
        res = app.test_client().delete(url)

    assert res.status_code == 200
    assert res.mimetype == "application/json"
    assert res.json == {"msg": "Executor %s succesfully deleted" % executor.id}


#############
# UTILS TESTS
#############

def test_date_trigger_to_dict():
    my_dt = arrow.get("2016-06-21T15:30:12").datetime
    trigger = DateTrigger(run_date=my_dt)
    trigger_dict = {"type": "date", "args": {"date": "2016-06-21T15:30:12+00:00"}}
    assert trigger_dict == trigger_to_dict(trigger)


def test_json_to_date_trigger():
    my_dt = arrow.get("2016-06-21T15:30:12").datetime
    trigger_dict = {"type": "date", "args": {"date": "2016-06-21T15:30:12+00:00"}}
    trigger = DateTrigger(run_date=my_dt)
    assert trigger.run_date == dict_to_trigger(trigger_dict).run_date
