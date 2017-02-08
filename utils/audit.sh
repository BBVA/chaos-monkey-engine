#! /bin/bash

set -e

docker run --entrypoint /opt/chaosmonkey/venv/bin/bandit --rm  chaos-monkey-engine -r -v /opt/chaosmonkey/src/chaosmonkey -f screen || /bin/true

