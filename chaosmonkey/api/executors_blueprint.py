"""
**Base path**: /api/1/executors

Executors are scheduled jobs that are related with an attack, so in the given date
the job will execute the attack.
The only way to create executors is through :meth:`chaosmonkey.api.plans_blueprint`

Evey executor has 4 main properties:

1. **id**: unique identifier
2. **next_run_time**: The time and date that the executor is going to be executed
3. **plan_id**: id of the plan that created the executor
4. **executed**: if the executor has been executed

Example::

    {
        "id": "3b373155577b4d1bbc62216ffea013a4",
        "plan_id": "3ec72048cab04b76bdf2cfd4bc81cd1e",
        "next_run_time": "2017-01-25T10:12:1485339145",
        "executed": false
    }

"""
import arrow
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.date import DateTrigger
from flask import Blueprint, json, request
from flask_hal import Document

from chaosmonkey.api.api_errors import APIError
from chaosmonkey.api.request_validator import validate_payload
from chaosmonkey.engine.cme_manager import manager
from chaosmonkey.api.utils import get_boolean

executors = Blueprint("executors", __name__)

executor_trigger_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "args": {
            "type": "object",
            "properties": {
                "date": {"type": "string"}
            },
            "required": ["date"]
        }
    },
    "required": ["type", "args"]
}


@executors.route("/", methods=["GET"])
def get_executors():
    """
    Get a list of scheduled executors

    Example response::

        {
            "executors":[
                {
                    "_links":{
                        "self":{
                            "href":"/api/1/executors/3b373155577b4d1bbc62216ffea013a4"
                        },
                        "update":{
                            "href":"/api/1/executors/3b373155577b4d1bbc62216ffea013a4"
                        },
                        "delete":{
                            "href":"/api/1/executors/3b373155577b4d1bbc62216ffea013a4"
                        }
                    },
                    "id":"3b373155577b4d1bbc62216ffea013a4",
                    "plan_id":"3ec72048cab04b76bdf2cfd4bc81cd1e",
                    "next_run_time":"2017-01-25T10:12:1485339145",
                    "executed": false
                }
            ]
        }

    :param: executed. Control when to show all executors (true) or only not executed (false). Defaults to false

    :return: :meth:`flask_hal.document`
    """
    executed_query = request.args.get("executed", False)
    executed = get_boolean(executed_query)
    executors_list = [executor.to_dict() for executor in manager.get_executors(executed=executed)]
    return Document(embedded={"executors": executors_list})


@executors.route("/<string:executor_id>", methods=['PUT'])
def put_executor(executor_id):
    """
    Update a executor to change its date. To provide a new date use the format
    in the example bellow.
    The format is used to create a
    `DateTrigger <https://github.com/agronholm/apscheduler/blob/master/apscheduler/triggers/date.py>`_
    from the apscheduler.

    TODO: create more `Triggers <https://github.com/agronholm/apscheduler/blob/master/apscheduler/triggers>`_

    Example request::

        PUT /api/1/executors/3b373155577b4d1bbc62216ffea013a4
        Body:
            {
              "type" : "date",
              "args" : {
                "date": "2017-10-23T19:19"
              }
            }

    Example response::

        {
          "id": "3b373155577b4d1bbc62216ffea013a4",
          "plan_id": "3ec72048cab04b76bdf2cfd4bc81cd1e",
          "next_run_time": "2017-10-23T19:19:1508786354",
          "executed": false,
          "_links": {
            "self": {
              "href": "/api/1/executors/3b373155577b4d1bbc62216ffea013a4"
            },
            "update":{
              "href":"/api/1/executors/3b373155577b4d1bbc62216ffea013a4"
            },
            "delete":{
              "href":"/api/1/executors/3b373155577b4d1bbc62216ffea013a4"
            }
          }
        }

    :return: :meth:`flask_hal.document`
    """
    assert validate_payload(request, executor_trigger_schema)
    body = request.get_json()

    trigger = dict_to_trigger(body)

    try:
        executor = manager.update_executor_trigger(executor_id, trigger)
    except JobLookupError:
        return json.jsonify({"msg": "executor not found " + executor_id}), 404
    else:
        return Document(data=executor.to_dict())


@executors.route("/<string:executor_id>", methods=['DELETE'])
def delete_executor(executor_id):
    """
    Delete an executor

    Example request::

        DEL /api/1/executors/6890192d8b6c40e5af16f13aa036c7dc
    """
    manager.remove_executor(executor_id)
    return json.jsonify({
        "msg": "Executor %s succesfully deleted" % executor_id
    })

########
# UTILS
#######


def trigger_to_dict(trigger):
    """
    Returns a dict version of the trigger
    """
    if isinstance(trigger, DateTrigger):
        trigger_dict = {}
        trigger_dict["type"] = "date"
        trigger_dict["args"] = {"date": arrow.get(trigger.run_date).isoformat()}
        return trigger_dict


def dict_to_trigger(trigger_dict):
    """
    Returns a trigger version of the trigger json
    """
    if trigger_dict["type"] == "date":
        if "args" not in trigger_dict:
            raise APIError("Missing trigger args")
        if "date" not in trigger_dict["args"]:
            raise APIError("Invalid trigger args")

        try:
            trigger = DateTrigger(run_date=arrow.get(trigger_dict["args"]["date"]).datetime)
        except arrow.parser.ParserError:
            raise APIError("Invalid date format")

        return trigger
    else:
        raise APIError("Invalid trigger type")
