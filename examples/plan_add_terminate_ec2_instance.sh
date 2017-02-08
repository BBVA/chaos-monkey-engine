#!/bin/bash

#
# Adds a plan with terminate_ec2_instance attack with the filter
# "Chaos=true". Using the simple_planner to schedule 4 executors
# between 10:00 and 17:00
#
# Usage:
#   ./plan_add_terminate_ec2_instance.sh
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/plans/"

readonly JSON='
{
    "name": "Terminate random instance with filter chaos=true",
    "attack":{
        "ref": "terminate_ec2_instance:TerminateEC2Instance",
        "args":{
            "region": "eu-west-1",
            "filters": {"tag:Chaos":"true"}
        }
    },
    "planner": {
        "ref":"simple_planner:SimplePlanner",
        "args": {
            "min_time" : "10:00",
            "max_time" : "17:00",
            "times": 4
        }
    }
}'

do_post() {
    echo ${JSON} | curl "$ENDPOINT" \
        -H "Content-Type:application/json" \
        --data @-
}

do_post
