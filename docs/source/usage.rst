.. _usage:

Usage
=====

Running ``cm --help`` shows the usage information::

  Usage: cm [OPTIONS]

    Chaos Monkey Engine command line utility

  Options:
    -p, --port INTEGER          Port used to expose the CM API
    -t, --timezone TEXT         Timezone to configure the scheduler
    -d, --database-uri TEXT     SQLAlchemy database uri  [required]
    -a, --attacks-folder TEXT   Path to the folder where the attacks are stored
                                [required]
    -p, --planners-folder TEXT  Path to the folder where the planners are stored
                                [required]
    --help                      Show this message and exit

- The **port** defaults to 5000
- The **timezone** defaults to ``Europe/Madrid``. The engine uses `pytz <https://pypi.python.org/pypi/pytz>`_ for managing the timezones.

The Docker container has a default ``CMD`` directive that sets these sane default options::

  "-d /opt/chaosmonkey/src/storage/cme.sqlite -a /opt/chaosmonkey/src/attacks -p /opt/chaosmonkey/src/planners"

For example, to launch the server on port 5000 TCP as a foreground process, passing AWS credentials::

  docker run --rm -p 5000:5000 -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION -ti cm

