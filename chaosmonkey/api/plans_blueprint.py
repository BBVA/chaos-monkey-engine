"""
**Base path**: /api/1/plans

Plans receive a planner and an attack and create executors calling the corresponding planner with the given
attack.

Each plan creates N executors related to an attack to be executed in the future.

Plans has the following properties

* **id**: unique identifier for a plan
* **created**: creation date
* **next_execution**: execution date for the next executor
* **name**: plan name
* **executors_count**: number of executors in the plan
* **executed**: if all the executors in the plan has been executed

"""
from flask import Blueprint, json, request
from flask_hal import Document
from chaosmonkey.api.request_validator import validate_payload
from chaosmonkey.engine.cme_manager import manager
from chaosmonkey.api.utils import get_boolean


plans = Blueprint("plans", __name__)

plan_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "attack": {
            "type": "object",
            "properties": {
                "ref": {"type": "string"},
                "args": {"type": "object"},
            },
            "required": ["ref", "args"]
        },
        "planner": {
            "type": "object",
            "properties": {
                "ref": {"type": "string"},
                "args": {"type": "object"},
            },
            "required": ["ref", "args"]
        }
    },
    "required": ["name", "attack", "planner"]
}


@plans.route("/", methods=["POST"])
def add_plan():
    """
    Add a plan.

    Example request::

        PUT /api/1/executors/3b373155577b4d1bbc62216ffea013a4
        Body:
            {
                "name": "Terminate instances in Playground",
                "attack": {
                    "args": {
                        "region": "eu-west-1",
                        "filters": {
                            "tag:Name": "playground-asg"
                        }
                    },
                    "ref": "terminate_ec2_instance:TerminateEC2Instance"
                },
                "planner": {
                    "ref": "simple_planner:SimplePlanner",
                    "args": {
                        "min_time" : "10:00",
                        "max_time" : "19:00",
                        "times": 4
                    }
                }
            }

    """
    assert validate_payload(request, plan_schema)
    req_json = request.get_json()

    name = req_json["name"]
    planner_config = req_json["planner"]
    attack_config = req_json["attack"]

    manager.execute_plan(name, planner_config, attack_config)

    return json.jsonify({"msg": "ok"})


@plans.route("/", methods=["GET"])
def list_plans():
    """
    List all plans created

    Example request::

        GET /api/1/plans/?all=true

    Example response::

        {
            "_links": {
                "self": {
                    "href": "/api/1/plans/"
                }
            },
            "plans": [
                {
                    "id": "6890192d8b6c40e5af16f13aa036c7dc",
                    "created": "2017-01-26T10:41:1485427282",
                    "next_execution": "2017-01-26 13:14:07.583372",
                    "name": "Terminate instances in Playground",
                    "executors_count": 2,
                    "_links": {
                        "self": {
                            "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc"
                        },
                        "update": {
                            "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc"
                        },
                        "delete": {
                            "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc"
                        }
                    }
                }
            ]
        }

    :param: all. Control when to show all plans (true) or only not executed (false). Defaults to false

    :return: :meth:`flask_hal.document`
    """
    show_all_query = request.args.get("all", False)
    show_all = get_boolean(show_all_query)
    plan_list = [plan.to_dict() for plan in manager.get_plans(show_all=show_all)]
    return Document(data={"plans": plan_list})


@plans.route("/<string:plan_id>", methods=["GET"])
def get_plan(plan_id):
    """
    Get a plan with all related executors

    Example request::

        GET /api/1/plans/6890192d8b6c40e5af16f13aa036c7dc

    Example response::

        {
            "id": "6890192d8b6c40e5af16f13aa036c7dc",
            "_embedded": {
                "executors": [
                    {
                        "plan_id": "6890192d8b6c40e5af16f13aa036c7dc",
                        "_links": {
                            "self": {
                                "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dcdd2530572fd04c5aa061f261f82743d3"
                            },
                            "update": {
                                "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dcdd2530572fd04c5aa061f261f82743d3"
                            },
                            "delete": {
                                "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dcdd2530572fd04c5aa061f261f82743d3"
                            }
                        },
                        "next_run_time": "2017-01-26T13:14:1485436447",
                        "id": "dd2530572fd04c5aa061f261f82743d3"
                    },
                    {
                        "plan_id": "6890192d8b6c40e5af16f13aa036c7dc",
                        "_links": {
                            "self": {
                                "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc1dd3f0d392e545808edb74852213c1ae"
                            },
                            "update": {
                                "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc1dd3f0d392e545808edb74852213c1ae"
                            },
                            "delete": {
                                "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc1dd3f0d392e545808edb74852213c1ae"
                            }
                        },
                        "next_run_time": "2017-01-26T18:24:1485455082",
                        "id": "1dd3f0d392e545808edb74852213c1ae"
                    }
                ]
            },
            "created": "2017-01-26T10:41:1485427282",
            "next_execution": null,
            "name": "Terminate instances in Playground",
            "executors_count": null,
            "_links": {
                "self": {
                    "href": "/api/1/plans/6890192d8b6c40e5af16f13aa036c7dc"
                }
            }
        }

    :return: :meth:`flask_hal.document`
    """
    plan = manager.get_plan(plan_id)
    executor_list = [executor.to_dict() for executor in manager.get_executors_for_plan(plan_id)]
    return Document(data=plan.to_dict(), embedded={"executors": executor_list})


@plans.route("/<string:plan_id>", methods=["DELETE"])
def delete_plan(plan_id):
    """
    Delete a plan

    Example request::

        DEL /api/1/plans/6890192d8b6c40e5af16f13aa036c7dc


    """
    manager.delete_plan(plan_id)
    return json.jsonify({
        "msg": "Plan %s successfully deleted" % plan_id
    })
