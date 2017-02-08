#!/bin/bash


#
# Get a list of all available planners
#
# Usage:
#   ./planners_list.sh
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/planners/"

get_plans() {
    curl "$ENDPOINT"
}

get_plans
