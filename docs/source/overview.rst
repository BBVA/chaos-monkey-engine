.. _overview:

Chaos Monkey Engine Overview
============================
The Chaos Monkey Engine (CME) is a tool to orchestrate attacks to your cloud infrastructure in order to implement the principles of `Chaos Engineering <http://principlesofchaos.org>`_. It is inspired in the Netflix's `SimianArmy <https://github.com/Netflix/SimianArmy>`_ but built with these principles in mind:

- Multi-cloud (not only AWS) support through standards as `Apache Libcloud <https://libcloud.apache.org/>`_ and SSH
- Ease of extensibility to add your new attacks and planners
- `HAL <https://en.wikipedia.org/wiki/Hypertext_Application_Language>`_ API interface

The CME is completely API-driven, so that it can be easily integrated with external and third-party systems.

Implementation
**************
The CME is a `Flask <http://flask.pocoo.org/>`_ application running with `gevent <http://www.gevent.org/>`_. It uses the `apscheduler <http://apscheduler.readthedocs.io/>`_ engine to schedule attacks and `SQLAlchemy <http://www.sqlalchemy.org/>`_ to persist the state of the attacks.

Arquitecture
************
The API has two main resources, planners and attacks. Trough the API you use planners to schedule jobs (named *executors*) that execute attacks. You can build your own planners and attacks to fit your needs.

In the other hand, in order to implement the attacks, you will need to interact with the cloud providers. Although it is not exactly required, we recommend using `apache-libcloud <https://libcloud.apache.org/>`_ (which is included as a dependency) in order to build reusable attacks abstracted from the underlying provider, using their cloud compute drivers. A working example of driver factory for EC2 is included in the CME package in order to interact with AWS EC2 instances.

Planners and Attacks
********************
Planners and attacks are the main resources of the engine. You create executors (scheduled attacks) using a planner and an attack definition.

The engine provides certain planners and attacks out of the box:

Planners
^^^^^^^^

Exact Planner
-------------
Reference: ``exact_planner:ExactPlanner``

A planner that schedules an executor for a specific date.

Example::

  "planner": {
    "ref":"exact_planner:ExactPlanner",
    "args": {
      "date":"2016-06-21T15:30:12+02:00"
    }
  }


Simple Planner
--------------
Reference: ``simple_planner:SimplePlanner``

A planner that schedules N executors for specific time range in today.

Example::

  "planner": {
    "ref":"simple_planner:SimplePlanner",
    "args": {
      "min_time" : "10:00",
      "max_time" : "18:00",
      "times": 4
    }
  }

Attacks
^^^^^^^

Terminate EC2 instance
----------------------
Reference: ``terminate_ec2_instance:TerminateEC2Instance``

Issues a terminate on a random EC2 instance filtered by any `AWS EC2 filter <http://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html#options>`_.

Example::

  "attack":{
    "ref": "terminate_ec2_instance:TerminateEC2Instance",
    "args":{
      "filters": {"tag:Chaos":"true"}
    }
  }

Terminate EC2 instance not excluded
-----------------------------------
Reference: ``terminate_ec2_instance:TerminateEC2InstanceNotExcluded``

Issues a terminate on a random EC2 instance filtered and excluding instances with `AWS filters <http://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html#options>`_.

Example::

  "attack":{
    "ref": "terminate_ec2_instance:TerminateEC2InstanceNotExcluded",
    "args":{
      "filters": {"tag:Chaos":"true"},
      "excluded": {"availability-zone":"eu-west-1"}
    }
  }

Api Request
-----------
Reference: ``api_request.ApiRequest``

Makes a request to any API endpoint.

Example::

  "attack":{
    "ref": "api_request.ApiRequest",
    "args": {
      "endpoint": "http://localhost:4500",
      "method": "GET",
      "payload": {"test": "1"},
      "headers": {"X-CUSTOM-HEADER": "test"},
    }
  }

Run script
----------

Reference: ``run_script:RunScript``

Runs a script on a random EC2 instance filtered by any AWS instance tag. The instance must be reachable by SSH.

Example::

  "attack":{
    "ref": "run_script:RunScript",
    "args": {
      "filters": {
        "tag:Chaos":"true"
      },
      "local_script": "script_attacks/s_burncpu.sh",
      "remote_script": "/chaos/burn_cpu",
      "ssh" : {
         "user": "ec2-user",
         "pem": "BASE64ENCODEDPEM"
      },
      "region": "eu-west-1"
    }
  }

The local script is uploaded to the ``remote_script`` destination and executed. The `pem` for the credentials is the Base64 encoded version of the file.

