.. _quickstart:

Quickstart
==========

This section will show how to deploy an initial Chaos Monkey Engine in a few minutes to test its functionality.

Chaos Monkey Engine
*******************

Chaos Monkey Engine helps you planning and executing attacks against any infrastructure. This helps you detecting
possible improvements in the mission of building an `antifragile <https://en.wikipedia.org/wiki/Antifragility>`_
infrastructure.


Requirements
************

* Docker 1.12+
* Amazon Web Services credentials in environment variables:

    * ``AWS_ACCESS_KEY_ID``
    * ``AWS_SECRET_ACCESS_KEY``
    * ``AWS_DEFAULT_REGION``


Get your engine up and running
******************************

Build and run the Docker container::

    docker build -t cm .
    docker run --rm -p 5000:5000 -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -ti cm

The Chaos Monkey Engine should be now listening in port 5000 TCP and ready to attack the machines in your AWS infrastructure.


Schedule a simple attack
************************

Create a plan file (``plan.json``) with a content similar to this one::

    {
        "name": "Terminate random running instance",
        "attack": {
            "ref": "terminate_ec2_instance:TerminateEC2Instance",
            "args": {
                "filters": {
                    "instance-state-name":"running"
                }
            }
        },
        "planner": {
            "args": {
                "min_time": "10:00",
                "max_time": "18:00",
                "times": 3
            },
        "ref": "simple_planner:SimplePlanner"
        }
    }


This plan schedules 3 attacks between 10:00 and 18:00 that terminate running EC2 instances of the region selected with ``AWS_DEFAULT_REGION``. You can use filters as described in the official `AWS documentation <http://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html#options>`_.

Send the plan to the engine::

    curl -X POST -H "Content-Type:application/json" -d @plan.json localhost:5000/api/1/plans/

Once the plan has been executed and the attack executors are created, you can check them issuing the following request::

    curl localhost:5000/api/1/executors/

Monitoring the output of the Chaos Monkey Engine, you will see the resulting executions.

