#!/bin/bash

#
# List all plans.
# Accepts 1 param to control the "all" filter.
#
# Usage:
#   ./plans_list.sh true
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/plans/?all=${1}"

get_plans() {
    curl "$ENDPOINT"
}

get_plans
