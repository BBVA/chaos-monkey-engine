#! /bin/bash

set -e

docker run --entrypoint /opt/chaosmonkey/venv/bin/python --rm chaos-monkey-engine -m pytest --cov=chaosmonkey -v /opt/chaosmonkey/src/test/unit/chaosmonkey -v /opt/chaosmonkey/src/attacks --root /opt/chaosmonkey/src/
docker run --entrypoint /opt/chaosmonkey/venv/bin/python --rm  chaos-monkey-engine -m pylint --rcfile=/opt/chaosmonkey/src/.pylintrc chaosmonkey || true

