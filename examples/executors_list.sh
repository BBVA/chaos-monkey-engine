#!/bin/bash

#
# Get a list of all executors
#
# Usage:
#   ./executors_list.sh true
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/executors/?executed=${1}"

get_plans() {
    curl "$ENDPOINT"
}

get_plans
