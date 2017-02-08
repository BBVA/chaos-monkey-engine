#!/bin/bash

#
# Get a list of all available attacks
#
# Usage:
#   ./attacks_list.sh
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/attacks/"

get_plans() {
    curl "$ENDPOINT"
}

get_plans
