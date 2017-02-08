Installation
============

There are two installation methods: Docker container (**recommended**) and Python package.

Docker container
****************

Build the container with Docker 1.12+::

    docker build -t cm .

Then, you can run the container as the ``cm`` command. E.g::

    docker run --rm cm --help

Python package
**************

Create a Python 3 `virtualenv <https://docs.python.org/3/library/venv.html>`_ before installing the package.

Install requirements::

    pip install -r requirements.txt

Install the engine::

    pip install .

Now you have the ``cm`` command on your path::

    cm --help

