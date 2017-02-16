Installation
============

There are two installation methods: Docker container (**recommended**) and Python package.

Docker container
****************

Build the container with Docker 1.12+::

    docker build -t chaos-monkey-engine .

Then, you can run the container as the ``chaos-monkey-engine`` command. E.g::

    docker run --rm chaos-monkey-engine --help

Python package
**************

You can install the latest package from `PyPi <https://pypi.python.org/pypi>`_::

    pip install chaosmonkey


Now you have the ``chaos-monkey-engine`` command on your path::

    chaos-monkey-engine --help

