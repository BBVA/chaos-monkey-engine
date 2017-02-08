# Scripts for running Chaos Monkey Engine

This is a collection of BASH scripts in order to help using the Chaos Monkey Engine as a Docker container for common tasks.


- `build.sh`: Build a Docker image named `chaos-monkey-engine`. It shoud run from the folder containing the Dockerfile
- `run.sh`: Launch the Docker contianer based on a local image named `chaos-monkey-engine`
- `test.sh`: Run the unit tests and [Pylint](https://www.pylint.org/)
- `audit.sh`: Run the [Bandit](https://wiki.openstack.org/wiki/Security/Projects/Bandit) audit
- `behave.sh`: Run the [behave](http://pythonhosted.org/behave/) based acceptance tests
