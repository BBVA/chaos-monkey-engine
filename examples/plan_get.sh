#!/bin/bash

#
# Get a plan detail
# Accepts 1 param for plan id
#
# Usage:
#   ./plan_get.sh PLAN_ID
#

source conf.sh

readonly ENDPOINT="$HOST/api/1/plans/${1}"

do_post() {
    curl "$ENDPOINT"
}

do_post
