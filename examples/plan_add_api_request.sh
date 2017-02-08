#!/bin/bash

#
# Adds a plan with api_request attack. Using the simple_planner to schedule 1 executors
# at 2017-02-07T10:30
#
# Usage:
#   ./plan_add_api_request.sh
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/plans/"

readonly JSON='
{
    "name": "API Attack",
    "attack": {
        "ref": "api_request:ApiRequest",
        "args": {
            "endpoint": "http://localhost:4500",
            "method": "POST",
            "payload": {"terminate": "1"},
            "headers": {"X-CUSTOM-HEADER": "test"}
        }
    },
    "planner": {
        "ref": "exact_planner:ExactPlanner",
        "args": {
            "date": "2017-02-07T10:30"
        }
    }
}'

do_post() {
    echo ${JSON} | curl "$ENDPOINT" \
        -H "Content-Type:application/json" \
        --data @-
}

echo ${JSON}
do_post
