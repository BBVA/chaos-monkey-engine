#!/bin/bash

#
# Adds a plan with run_script attack. Using the simple_planner to schedule 2 executors
# between 10:00 and 18:00
#
# Usage:
#   ./plan_add_run_script.sh ~/certs/aws.pem
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/plans/"

AUTH=$(cat $1 | base64)

readonly JSON='
{
    "name": "Empty Script in random instance with filter ",
    "attack": {
        "ref": "run_script:RunScript",
        "args": {
            "filters": {
                "tag:Chaos":"true"
            },
            "local_script": "'$(pwd)'/script_attacks/s_burncpu.sh",
            "remote_script": "/chaos/burn_cpu",
            "ssh" : {
                "user": "ec2-user",
                "pem": "'$AUTH'"
            },
            "region": "eu-west-1"
        }
    },
    "planner": {
        "ref": "simple_planner:SimplePlanner",
        "args": {
            "min_time" : "10:00",
            "max_time" : "18:00",
            "times": 2
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
