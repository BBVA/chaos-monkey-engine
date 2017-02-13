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


Or you can install the package locally from source code.

Create a Python 3 `virtualenv <https://docs.python.org/3/library/venv.html>`_ before installing the package.

Install requirements::

    pip install -r requirements.txt

Install the engine::

    pip install .

Now you have the ``chaos-monkey-engine`` command on your path::

    chaos-monkey-engine --help

