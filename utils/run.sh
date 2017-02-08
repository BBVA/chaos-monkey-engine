#! /bin/bash

docker run --rm -p 5000:5000 -v $(pwd)/storage:/opt/chaosmonkey/src/storage -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -ti chaos-monkey-engine $@


