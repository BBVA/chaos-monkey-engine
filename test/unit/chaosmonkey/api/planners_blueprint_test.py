from flask import url_for
from flask_hal import Document
import test.planners.planner1 as planner1_module
import test.planners.planner2 as planner2_module


def test_empty_planners_store_return_hal(app, manager):
    url = url_for("planners.list_planners")

    planners_list = []
    manager.planners_store.set_modules(planners_list)

    with app.test_request_context(url):
        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(data={"planners": []}).to_dict()


def test_planners_list_return_hal(app, manager):
    url = url_for("planners.list_planners")

    module_list = [planner1_module, planner2_module]
    manager.planners_store.set_modules(module_list)

    with app.test_request_context(url):

        planner_list = [planner1_module.Planner1("planner1").to_dict(), planner2_module.Planner2("planner2").to_dict()]

        res = app.test_client().get(url)
        assert res.status_code == 200
        assert res.mimetype == "application/hal+json"
        assert res.json == Document(data={"planners": planner_list}).to_dict()
