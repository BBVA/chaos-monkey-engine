"""
**Base path**: /api/1/planners

Planners are python modules (located in /planners folder). Planners are responsible of create
:meth:`executors <chaosmonkey.api.executors_blueprint>`.

Planners has three main properties represented in the API:

1. **example**:  a JSON example for the planner
2. **ref**: its unique identifier. module_name:PlannerClass
3. **schema**: json schema that validates the planner

"""
from flask import Blueprint
from flask_hal import Document
from chaosmonkey.engine.cme_manager import manager

planners = Blueprint("planners", __name__)


@planners.route("/", methods=["GET"])
def list_planners():
    """
    Return a list with the available planners and its configuration.

    Example response::

        {
            "_links": {
                "self": {
                    "href": "/api/1/planners/"
                }
            },
            "planners": [
                {
                    "example": {
                        "args": {
                            "times": 4,
                            "max_time": "15:00",
                            "min_time": "10:00"
                        },
                        "ref": "simple_planner:SimplePlanner"
                    },
                    "ref": "simple_planner:SimplePlanner",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "args": {
                                "type": "object",
                                "properties": {
                                    "times": {
                                        "type": "number"
                                    },
                                    "max_time": {
                                        "type": "string"
                                    },
                                    "min_time": {
                                        "type": "string"
                                    }
                                }
                            },
                            "ref": {
                                "type": "string"
                            }
                        }
                    }
                }
            ]
        }

    :return: :meth:`flask_hal.document`
    """
    planners_list = manager.get_planner_list()
    return Document(data={"planners": planners_list})
