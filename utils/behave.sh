#! /bin/bash

set -e

docker run \
	--entrypoint /opt/chaosmonkey/venv/bin/behave \
	-e AWS_SECRET_ACCESS_KEY -e AWS_ACCESS_KEY_ID \
	--rm  \
	chaos-monkey-engine /opt/chaosmonkey/src/test/acceptance/features -D root=/opt/chaosmonkey/src/

