from datetime import datetime, timedelta
from flask import url_for, json
from flask_hal import Document
import test.attacks.attack1 as attack1_module
import test.planners.planner1 as planner1_module

valid_request_body = {
    "name": "Test Planner",
    "attack": {
        "ref": "test.attacks.attack1:Attack1",
        "args": {}
    },
    "planner": {
        "ref": "test.planners.planner1:Planner1",
        "args": {}
    }
}


def test_empty_plans_return_hal(app):
    url = url_for("plans.list_plans")

    with app.test_request_context(url):
        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(data={"plans": []}).to_dict()


def test_plan_list_return_hal(app, manager):
    url = url_for("plans.list_plans")

    plan = manager.add_plan("plan name")

    with app.test_request_context(url):

        plan_list = [plan.to_dict()]

        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(data={"plans": plan_list}).to_dict()


def test_plan_get_return_hal_with_executors(app, manager):
    plan = manager.add_plan("plan name")
    run_time = datetime.now() + timedelta(hours=10)
    executor = manager.add_executor(run_time, "executor name", {}, plan.id)

    url = url_for("plans.get_plan", plan_id=plan.id)

    with app.test_request_context(url):
        res = app.test_client().get(url)

        expected = Document(data=plan.to_dict(), embedded={"executors": [executor.to_dict()]}).to_dict()

        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == expected


def test_plan_add_valid_body(app, manager):
    url = url_for("plans.add_plan")

    # add a planner and an attack
    manager.attacks_store.add(attack1_module)
    manager.planners_store.add(planner1_module)

    with app.test_request_context(url):

        res = app.test_client().post(url_for("plans.add_plan"),
                                     content_type="application/json",
                                     data=json.dumps(valid_request_body))

        assert res.status_code == 200
        assert res.mimetype == "application/json"
        assert res.json == {"msg": "ok"}
